from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

api = Api(
    app,
    title="C# Deep Tutor API Gateway",
    version="1.0",
    description="AWS Flask 서버에서 ngrok을 통해 Colab LLM 서버로 요청을 전달하는 API"
)

chat_ns = api.namespace(
    "chat",
    description="LLM Chat API"
)

health_ns = api.namespace(
    "health",
    description="Server Health Check API"
)

version_ns = api.namespace(
    "version",
    description="API Version Check"
)

chat_request = api.model("ChatRequest", {
    "prompt": fields.String(
        required=True,
        description="사용자 질문",
        example="스택과 큐의 차이를 설명해줘"
    ),
    "history": fields.List(
        fields.Raw,
        required=False,
        description="이전 대화 기록"
    )
})

chat_response = api.model("ChatResponse", {
    "response": fields.String(
        description="LLM 응답"
    )
})

health_response = api.model("HealthResponse", {
    "status": fields.String(description="서버 상태"),
    "llm_server": fields.String(description="Colab LLM 서버 연결 상태")
})

version_response = api.model("VersionResponse", {
    "api_name": fields.String(description="API 이름"),
    "version": fields.String(description="API 버전"),
    "model": fields.String(description="사용 모델")
})

LOCAL_LLM_URL = "https://cloud-dynamite-mandolin.ngrok-free.dev/chat"
LOCAL_LLM_HEALTH_URL = "https://cloud-dynamite-mandolin.ngrok-free.dev/health"


@health_ns.route("")
class Health(Resource):

    @health_ns.doc(description="AWS API 서버와 Colab LLM 서버 연결 상태를 확인합니다.")
    @health_ns.marshal_with(health_response)
    def get(self):
        try:
            res = requests.get(
                LOCAL_LLM_HEALTH_URL,
                timeout=10
            )

            if res.status_code == 200:
                llm_status = "connected"
            else:
                llm_status = "error"

        except Exception:
            llm_status = "disconnected"

        return {
            "status": "aws api server running",
            "llm_server": llm_status
        }


@version_ns.route("")
class Version(Resource):

    @version_ns.doc(description="API 서버 버전과 모델 정보를 반환합니다.")
    @version_ns.marshal_with(version_response)
    def get(self):
        return {
            "api_name": "C# Deep Tutor API Gateway",
            "version": "1.0",
            "model": "fine-tuned Llama3.2 C# data structure model"
        }


@chat_ns.route("")
class Chat(Resource):

    @chat_ns.doc(description="사용자 질문을 Colab LLM 서버로 전달하고 응답을 반환합니다.")
    @chat_ns.expect(chat_request)
    @chat_ns.marshal_with(chat_response)
    def post(self):
        data = request.get_json()

        try:
            start_time = time.time()

            response = requests.post(
                LOCAL_LLM_URL,
                json=data,
                timeout=300
            )

            response.raise_for_status()

            result = response.json()

            return {
                "response": result.get("response", "")
            }

        except Exception as e:
            return {
                "response": f"AWS 서버에서 LLM 서버 연결 실패: {str(e)}"
            }, 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )