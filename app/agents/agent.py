from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GOOGLE_API_KEY
from app.core.logger import logger
from app.agents.tools.search_tool import search_tool
from app.agents.tools.booking_tool import booking_tool
from app.agents.tools.summarization_tool import summarize_tool
from app.memory.user_memory import get_user_memory  # ✅ 사용자 메모리 가져오기

class ReservationAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            google_api_key=GOOGLE_API_KEY
        )
        logger.info("✅ ReservationAgent 초기화 완료")

    async def run(self, user_input: str, user_id: int) -> str:
        logger.info(f"🧠 ReservationAgent 실행: {user_input}")

        memory = get_user_memory(user_id)  # ✅ 사용자별 메모리 가져오기

        try:
            agent = initialize_agent(
                tools=[search_tool, booking_tool, summarize_tool],
                llm=self.llm,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                memory=memory,
                verbose=True
            )
            result = await agent.arun(user_input)
            logger.info(f"[{user_id}] 🤖 응답: {result}")
            return result
        except Exception as e:
            logger.exception(f"❌ 에이전트 실행 중 오류 발생: {e}")
            return "요청 처리 중 문제가 발생했습니다."