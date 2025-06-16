from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GOOGLE_API_KEY
from app.core.logger import logger

class IntentService:
    def __init__(self):
        # Gemini 2.0 Flash 모델 사용 (2025년 기준 최신)
        #  - 빠른 응답 속도 + 1M context 지원, 테스트용으로 적당함
        # temperature=0은 항상 비슷한 응답을 하도록 만드는 설정
        #  - 숫자가 높으면 창의적으로 답변 (일반적으로 0.0부터 1.0)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            google_api_key=GOOGLE_API_KEY
        )

    async def analyze_intent(self, user_input: str) -> str:
        prompt = f"""
        너는 사용자의 요청을 분석하는 의도 분석기야.
        아래 요청이 '검색', '처리', '기타' 중 어떤 Intent 인지 하나로 답해줘.

        요청: {user_input}

        의도:
        """
        response = self.llm.invoke(prompt)
        logger.info(f"사용자 요청 분석: {response}")
        return response.content.strip()
