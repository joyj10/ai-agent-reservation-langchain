from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agents.tools.booking_tool import booking_tool
from app.agents.tools.search_tool import search_tool
from app.agents.tools.summarization_tool import summarize_tool
from app.core.config import GOOGLE_API_KEY
from app.core.logger import logger
from app.memory.user_memory import get_user_memory
from app.models.user_info import UserInfo


class ReservationAgent:
    def __init__(self):
        ChatGoogleGenerativeAI.model_rebuild()

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            google_api_key=GOOGLE_API_KEY,
        )

        self.tools = [
            booking_tool,
            search_tool,
            summarize_tool,
        ]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "당신은 사용자의 요청에 따라 장소 예약을 생성, 수정, 취소하는 비서입니다."),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # 최신 방식: create_tool_calling_agent + AgentExecutor
        agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

        logger.info("✅ ReservationAgent 초기화 완료")

    async def run(self, user_input: str, user_info: UserInfo) -> str:
        logger.info(f"🧠 ReservationAgent 실행: {user_input}")
        user_id = user_info.user_id
        memory = get_user_memory(user_id)

        try:
            result = await self.agent_executor.ainvoke(
                {
                    "input": user_input,
                    "user_info": user_info,
                },
                config={"configurable": {"memory": memory}},
            )
            logger.info(f"[{user_id}] 🤖 응답: {result}")
            return result.get("output", "요청 처리 중 문제가 발생했습니다.")
        except Exception as e:
            logger.exception(f"❌ 에이전트 실행 중 오류 발생: {e}")
            return "요청 처리 중 문제가 발생했습니다."