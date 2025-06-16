from app.agents.tools.search_tool import SearchTool
from app.agents.tools.booking_tool import BookingTool
from app.agents.tools.summarization_tool import SummarizationTool
from app.core.logger import logger

class ReservationAgent:
    def __init__(self):
        self.search_tool = SearchTool()
        self.booking_tool = BookingTool()
        self.summarization_tool = SummarizationTool()
        logger.info("=== ReservationAgent 초기화 완료 ===")

    async def run(self, user_input: str, intent: str) -> str:
        logger.info(f"ReservationAgent run() 호출됨 - intent: {intent}, user_input: {user_input}")

        try:
            if intent == "검색":
                return await self.search_tool.search(user_input)
            elif intent == "처리":
                return await self.booking_tool.process_booking(user_input)
            elif intent == "기타":
                return await self.summarization_tool.summarize(user_input)
            else:
                logger.warning(f"알 수 없는 intent 수신: {intent}")
                return "알 수 없는 요청입니다."
        except Exception as e:
            logger.exception(f"ReservationAgent run() 중 예외 발생: {e}")
            return "처리 중 오류가 발생했습니다."
