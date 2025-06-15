from app.agents.tools.search_tool import SearchTool
from app.agents.tools.booking_tool import BookingTool
from app.agents.tools.summarization_tool import SummarizationTool

class ReservationAgent:
    def __init__(self):
        self.search_tool = SearchTool()
        self.booking_tool = BookingTool()
        self.summarization_tool = SummarizationTool()

    async def run(self, user_input: str, intent: str) -> str:
        if intent == "검색":
            return await self.search_tool.search(user_input)
        elif intent == "처리":
            return await self.booking_tool.process_booking(user_input)
        elif intent == "기타":
            return await self.summarization_tool.summarize(user_input)
        else:
            return "알 수 없는 요청입니다."
