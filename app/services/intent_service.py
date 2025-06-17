from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GOOGLE_API_KEY
from app.core.logger import logger
from app.memory.user_memory import get_user_memory


class IntentService:
    def __init__(self):
        # Gemini 2.0 Flash 모델 사용 (2025년 기준 최신)
        # - temperature=0은 항상 비슷한 응답을 하도록 만드는 설정
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            google_api_key=GOOGLE_API_KEY
        )

        # Prompt 템플릿 정의
        self.prompt = PromptTemplate(
            input_variables=["chat_history", "user_input"],
            template="""
        너는 사용자의 요청을 분석하는 의도 분석기야.
        다음은 지금까지의 대화야:
        {chat_history}
        
        사용자 요청: {user_input}
        
        이 요청의 의도는 다음 중 하나야: '검색', '예약처리', '기타'.
        의도를 하나만 명확하게 말해줘.
        
        의도:
        """
        )

    async def analyze_intent(self, user_input: str, user_id: int) -> str:
        memory = get_user_memory(user_id)

        # 체인 구성
        chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=memory,
            verbose=False
        )

        # 체인 실행(메모리 자동 업데이트)
        response = await chain.arun(user_input=user_input)
        logger.info(f"[{user_id}] 사용자 요청 분석: {response}")
        return response.strip()
