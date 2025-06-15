from app.services.intent_service import IntentService
from app.agents.agent import ReservationAgent

class AgentService:
    def __init__(self):
        self.intent_service = IntentService()
        self.agent = ReservationAgent()

    async def handle_request(self, user_input: str) -> str:
        intent = await self.intent_service.analyze_intent(user_input)
        result = await self.agent.run(user_input, intent)
        return result
