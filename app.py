# from flask import Flask, request
# from flask_restx import Api, Resource, fields
# from flask_cors import CORS

# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM

# app = Flask(__name__)
# CORS(app)

# api = Api(
#     app,
#     title="C# Deep Tutor API",
#     version="1.0",
#     description="Fine-tuned Llama3.2 기반 C# 자료구조 튜터 API"
# )

# chat_ns = api.namespace(
#     "chat",
#     description="C# Deep Tutor Chat API"
# )

# chat_request = api.model("ChatRequest", {
#     "prompt": fields.String(required=True, description="사용자 질문"),
#     "history": fields.List(fields.Raw, required=False, description="이전 대화 기록")
# })

# chat_response = api.model("ChatResponse", {
#     "response": fields.String(description="모델 응답")
# })


# MODEL_PATH = "outputs/final_csharp_cs_model"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# quant_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_compute_dtype=torch.float16,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_use_double_quant=True
# )

# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_PATH,
#     quantization_config=quant_config,
#     device_map="auto"
# )

# model.eval()


# @chat_ns.route("")
# class Chat(Resource):

#     @chat_ns.expect(chat_request)
#     @chat_ns.marshal_with(chat_response)
#     def post(self):
#         data = request.get_json()

#         user_prompt = data.get("prompt", "")

#         prompt = f"""당신은 C# 자료구조를 깊이 있게 설명하는 시니어 개발자입니다.
# 답변은 한국어로 하고, 실무 관점과 C# 내부 동작을 함께 설명하세요.

# 질문:
# {user_prompt}

# 답변:
# """

#         inputs = tokenizer(
#             prompt,
#             return_tensors="pt"
#         ).to(model.device)

#         with torch.no_grad():
#             outputs = model.generate(
#                 **inputs,
#                 max_new_tokens=400,
#                 temperature=0.4,
#                 top_p=0.85,
#                 repetition_penalty=1.2,
#                 do_sample=True,
#                 pad_token_id=tokenizer.eos_token_id
#             )

#         result = tokenizer.decode(
#             outputs[0],
#             skip_special_tokens=True
#         )

#         # 프롬프트 부분 제거
#         if "답변:" in result:
#             result = result.split("답변:", 1)[-1].strip()

#         return {
#             "response": result
#         }


# if __name__ == "__main__":
#     app.run(
#         host="0.0.0.0",
#         port=8001,
#         debug=False
#     )




from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

api = Api(app)

chat_ns = api.namespace("chat")

chat_request = api.model("ChatRequest", {
    "prompt": fields.String(required=True),
    "history": fields.List(fields.Raw, required=False)
})

chat_response = api.model("ChatResponse", {
    "response": fields.String()
})

LOCAL_LLM_URL = "https://cloud-dynamite-mandolin.ngrok-free.dev"

@chat_ns.route("")
class Chat(Resource):
    @chat_ns.expect(chat_request)
    @chat_ns.marshal_with(chat_response)
    def post(self):
        data = request.get_json()

        response = requests.post(
            LOCAL_LLM_URL,
            json=data,
            timeout=120
        )

        return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)