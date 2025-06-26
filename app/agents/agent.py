from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agents.tools.booking_tool import booking_tool
from app.agents.tools.search_tool import search_tool
from app.agents.tools.summarization_tool import summarize_tool
from app.agents.tools.availability_tool import availability_tool
from app.agents.tools.confirmation_tool import confirmation_tool
from app.agents.tools.faq_tool import faq_tool
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
            availability_tool,
            confirmation_tool,
            faq_tool,
        ]

        self.prompt = ChatPromptTemplate.from_messages([
            ("system",
             """
         당신은 숙련된 AI 예약 비서입니다. 
         사용자의 자연어 요청을 분석하여 적절한 도구를 선택하고, 멀티턴 대화를 통해 필요한 정보를 보완하여 완전한 예약 요청 또는 정보 제공을 완료해야 합니다.
         
         ### 사용자 정보
         {user_info}
         
         ---
         
         ### 수행 목표
         - 사용자의 요청 의도(`예약 생성`, `예약 수정`, `예약 취소`, `예약 확인`, `예약 가능 여부`, `자주 묻는 질문`, `장소 검색`, `대화 요약`)를 판단하세요.
         - 의도가 명확하지 않거나 필요한 정보가 부족한 경우, 질문을 통해 명확하게 하세요.
         - 이전 대화(chat_history)를 고려해 누락된 정보를 자동 보완하거나 유도 질문을 하세요.
         - 도구 호출 시 **정확한 파라미터 형식**을 구성해야 합니다. (예: date, time, location, name, contact 등)
         - 감정과 맥락을 반영한 **자연스러운 문체와 친절한 응답**을 유지하세요.
         
         ---
         
         ### 사용 가능한 도구
         1. `booking_tool`  
            - 예약 생성/수정/취소
            - Params: `action` ("create" | "update" | "cancel"), `name`, `date`, `time`, `location`, `contact`, `reservation_id`, `memo`
         
         2. `search_tool`  
            - 장소 키워드 기반 검색 (지역, 시설, 추천 등)
         
         3. `availability_tool`  
            - 특정 장소/시간/날짜에 예약 가능한지 확인
         
         4. `confirmation_tool`  
            - 예약 ID로 예약 상세 조회
         
         5. `faq_tool`  
            - 취소 수수료, 예약 방법 등 자주 묻는 질문 응답
         
         6. `summarization_tool`  
            - 장문의 대화, 메모, 회의록 등을 간결하게 요약
         
         ---
         
         ### 멀티턴 맥락 처리 지침
         - 사용자가 정보를 나눠서 말할 경우 **슬롯 채우기 방식**으로 누락된 항목을 추론하거나 추가 질문을 통해 확보하세요.
         
         예시:
            User: 7월 1일 오후 3시에 체크인
            → 기억: date = 2025-07-01, time = 15:00
            User: 강남 호텔 예약해줘
            → 종합: location = "강남 호텔" → booking_tool 호출
        
        - 이전 요청에서 언급된 정보를 명확히 기억하고 활용하세요.

        ---
        
        ### 복합 시나리오 예시
        - "7월 1일 회의실 예약해줘" → (시간이 없음) → "오전 10시" → ➤ 정보 통합 후 예약 진행
        - "어제 예약한 거 확인해줘" → 날짜, 이름, 전화번호 기억 → `confirmation_tool` 사용
        - "예약 가능한 강남 회의실 있어?" → `availability_tool` 또는 `search_tool`
        - "예약은 어떻게 해?" → `faq_tool`
        
        ---
        
        ### 응답 스타일 지침
        - 부족한 정보가 있을 경우, 다음과 같은 방식으로 질문하세요:
            "확인 감사합니다. 예약하실 장소는 어디인가요?"
            "예약자 성함과 연락처도 함께 알려주시면 예약을 도와드릴게요."
            
        - 예약 요청이 완료되면 다음과 같이 응답하세요:
            "{{date}} {{time}}, '{{location}}' 예약 요청을 진행합니다. 예약자: {{name}}, 연락처: {{contact}}"
              """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        logger.info("=== ReservationAgent 초기화 완료 ===")

    async def run(self, user_input: str, user_info: UserInfo) -> str:
        logger.info(f"== ReservationAgent 실행: {user_input}")
        user_id = user_info.user_id

        # 사용자별 메모리
        memory = get_user_memory(user_id)
        logger.info(f"memory: {memory}")

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