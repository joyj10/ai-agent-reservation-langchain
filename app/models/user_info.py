from pydantic import BaseModel

class UserInfo(BaseModel):
    user_id: int
    name: str
    contact: str
