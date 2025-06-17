from app.services.intent_service import IntentService
from app.agents.agent import ReservationAgent

class AgentService:
    def __init__(self):
        self.intent_service = IntentService()
        self.agent = ReservationAgent()

    async def handle_request(self, user_input: str, user_id: int) -> str:
        intent = await self.intent_service.analyze_intent(user_input, user_id)
        result = await self.agent.run(user_input, intent)
        return result
