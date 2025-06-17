from app.agents.agent import ReservationAgent

class AgentService:
    def __init__(self):
        self.agent = ReservationAgent()

    async def handle_request(self, user_input: str, user_id: int) -> str:
        result = await self.agent.run(user_input, user_id)
        return result