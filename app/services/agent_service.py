from app.agents.agent import ReservationAgent
from app.models.user_info import UserInfo


class AgentService:
    def __init__(self):
        self.agent = ReservationAgent()

    async def handle_request(self, user_input: str, user_info: UserInfo) -> str:
        result = await self.agent.run(user_input, user_info)
        return result