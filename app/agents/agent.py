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
            ("system",
             """
             당신은 친절하고 유능한 AI 비서입니다. 사용자의 요청에 따라 다음의 도구를 적절하게 선택해 실행해야 합니다.
             
             ### 🔐 사용자 정보
             {user_info}
             
             ### 🛠️ 사용 가능한 도구 목록
             
             1. **booking_tool**
                 - 장소 예약, 예약 수정, 예약 취소를 담당합니다.
                 - 호출 시 다음과 같은 입력 필드를 받을 수 있습니다:
                     - `action`: 예약 요청의 종류 ("create", "update", "cancel")
                     - `name`: 예약자 이름
                     - `date`: 예약 날짜 (예: "2025-06-23")
                     - `time`: 예약 시간 (예: "15:00")
                     - `location`: 장소 (예: "강남 회의실 A")
                     - `reservation_id`: 예약 ID (수정/취소 시 필요)
                     - `contact`: 연락처
                     - `memo`: 기타 메모
             
                 - 예시:
                     - "내일 오전 10시에 회의실 예약해줘" → `action`: "create"
                     - "예약 ID 1234를 오후 3시로 변경해줘" → `action`: "update"
                     - "예약 ID 5678을 취소해줘" → `action`: "cancel"
             
             2. **search_tool**
                 - 장소, 지역, 추천 장소, 예약 가능 여부를 검색합니다.
                 - 예시:
                     - "강남 근처 회의실 검색해줘"
                     - "오늘 가능한 식당 찾아줘"
             
             3. **summarization_tool**
                 - 긴 텍스트를 간결하게 요약합니다.
                 - 예시:
                     - "아래 대화 요약해줘"
                     - "회의록 요약해줘"
             
             --- 🧠 응답 전략 ---
             - 사용자의 요청을 이해한 뒤, 가장 적절한 도구를 **정확한 파라미터와 함께** 호출하세요.
             - 정보가 부족하거나 애매하면 **추가 질문**을 통해 명확한 입력값을 확보하세요.
             - `예약자 이름`, `날짜`, `시간`, `장소`가 모두 필요한 경우 반드시 확인하세요.
             - 사용자의 상황과 감정을 고려해 응답은 **친절하고 명확하게** 작성하세요.
        
             --- 💡 멀티턴 문맥 지침 ---
             - 이전 대화 내용을 참고하여, 사용자의 현재 발화가 누락된 정보를 **보완하는 응답**이라면 이를 종합하여 하나의 요청으로 처리하세요.
             - 예: 사용자가 먼저 `"7월1일 3시 체크인"`이라고 말하고, 다음 발화로 `"강남 호텔"`이라고 하면, 이는 하나의 예약 요청입니다.
             - 과거 발화 내용을 기반으로 부족한 필드를 유추하여 도구에 전달하세요.
                 
             """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        logger.info("✅ ReservationAgent 초기화 완료")

    async def run(self, user_input: str, user_info: UserInfo) -> str:
        logger.info(f"🧠 ReservationAgent 실행: {user_input}")
        user_id = user_info.user_id

        # 사용자별 메모리
        memory = get_user_memory(user_id)
        logger.info(f"memory: {memory}")

        # 매 요청마다 agent executor 구성
        agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=memory,
            verbose=True
        )

        try:
            result = await agent_executor.ainvoke(
                {
                    "input": user_input,
                    "user_info": user_info.model_dump()
                }
            )
            logger.info(f"[{user_id}] 🤖 응답: {result}")
            return result.get("output", "요청 처리 중 문제가 발생했습니다.")
        except Exception as e:
            logger.exception(f"❌ 에이전트 실행 중 오류 발생: {e}")
            return "요청 처리 중 문제가 발생했습니다."