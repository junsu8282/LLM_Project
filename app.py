import threading

import torch
from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Namespace, Resource, fields
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

MODEL_PATH = "/home/juns/LLM_Project/models/phase2_merged_v3"

SYSTEM_PROMPT = (
    "당신은 개발 개념을 설명하는 AI 튜터입니다. "
    "개발 관련 질문에는 정의, 동작 방식, 장점, 단점, 사용 예시를 "
    "중심으로 설명하세요. "
    "일반 질문에는 자연스럽고 간결하게 답변하세요."
)

# 동시에 여러 generate()가 실행되는 것을 방지
generation_lock = threading.Lock()


# =========================================================
# 모델 로딩
# 서버 실행 시 한 번만 로딩됩니다.
# =========================================================

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

print("토크나이저 로딩 중...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    local_files_only=True,
)

if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token

print("모델 로딩 중...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    quantization_config=bnb_config,
    device_map="auto",
    local_files_only=True,
)

model.eval()

# device_map="auto"를 사용하는 경우 입력을 첫 번째 모델 장치로 이동
input_device = next(model.parameters()).device

print(f"모델 로딩 완료: {input_device}")


# =========================================================
# 프롬프트 생성
# history 형식:
# [
#     {"role": "user", "content": "안녕"},
#     {"role": "assistant", "content": "안녕하세요"}
# ]
# =========================================================

def build_prompt(prompt: str, history: list[dict]) -> str:
    prompt_parts = [
        f"system: {SYSTEM_PROMPT}",
    ]

    # 너무 긴 대화로 인한 메모리 증가 방지
    recent_history = history[-6:]

    for message in recent_history:
        role = message.get("role")
        content = str(message.get("content", "")).strip()

        if not content:
            continue

        if role == "user":
            prompt_parts.append(f"user: {content}")

        elif role == "assistant":
            prompt_parts.append(f"assistant: {content}")

    prompt_parts.append(f"user: {prompt.strip()}")
    prompt_parts.append("assistant:")

    return "\n".join(prompt_parts)


def clean_answer(answer: str) -> str:
    stop_words = [
        "\nuser:",
        "\nsystem:",
        "\nassistant:",
        "<|end_of_text|>",
    ]

    for stop_word in stop_words:
        if stop_word in answer:
            answer = answer.split(stop_word, 1)[0]

    return answer.strip()


def generate_answer(prompt: str, history: list[dict]) -> str:
    full_prompt = build_prompt(prompt, history)

    inputs = tokenizer(
        full_prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1536,
    )

    inputs = {
        key: value.to(input_device)
        for key, value in inputs.items()
    }

    input_length = inputs["input_ids"].shape[-1]

    with generation_lock:
        with torch.inference_mode():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False,
                repetition_penalty=1.1,
                no_repeat_ngram_size=3,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )

    generated_tokens = outputs[0][input_length:]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    )

    return clean_answer(answer)


# =========================================================
# Flask-RESTX 설정
# =========================================================

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": "*"
        }
    },
)

api = Api(
    app,
    version="1.0",
    title="Developer Tutor LLM API",
    description="phase2_merged_v3 모델 추론 서버",
    doc="/docs",
)

chat_ns = Namespace(
    "chat",
    description="LLM 채팅 API",
)

health_ns = Namespace(
    "health",
    description="서버 상태 확인 API",
)

api.add_namespace(chat_ns)
api.add_namespace(health_ns)


history_message_model = api.model(
    "HistoryMessage",
    {
        "role": fields.String(
            required=True,
            enum=["user", "assistant"],
            example="user",
        ),
        "content": fields.String(
            required=True,
            example="큐가 뭐야?",
        ),
    },
)

chat_request_model = api.model(
    "ChatRequest",
    {
        "prompt": fields.String(
            required=True,
            description="현재 사용자의 질문",
            example="스택과 큐의 차이를 설명해줘",
        ),
        "history": fields.List(
            fields.Nested(history_message_model),
            required=False,
            description="이전 대화 기록",
        ),
    },
)

chat_response_model = api.model(
    "ChatResponse",
    {
        "answer": fields.String(
            description="모델이 생성한 답변",
        ),
    },
)


@chat_ns.route("")
class ChatResource(Resource):

    @chat_ns.expect(chat_request_model, validate=True)
    @chat_ns.marshal_with(chat_response_model, code=200)
    def post(self):
        """LLM 답변 생성"""

        data = request.get_json(silent=True) or {}

        prompt = str(data.get("prompt", "")).strip()
        history = data.get("history") or []

        if not prompt:
            chat_ns.abort(
                400,
                "prompt 값이 비어 있습니다.",
            )

        try:
            answer = generate_answer(
                prompt=prompt,
                history=history,
            )

            return {
                "answer": answer,
            }, 200

        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()

            chat_ns.abort(
                503,
                "GPU 메모리가 부족합니다.",
            )

        except Exception as error:
            print(f"추론 오류: {error}")

            chat_ns.abort(
                500,
                f"모델 추론 중 오류가 발생했습니다: {str(error)}",
            )


@health_ns.route("")
class HealthResource(Resource):

    def get(self):
        """서버 상태 확인"""

        return {
            "status": "ok",
            "model": "phase2_merged_v3",
            "device": str(input_device),
        }, 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
        threaded=True,
    )