from pydantic import BaseModel

class AgentRequest(BaseModel):
    user_input: str
    user_id: int