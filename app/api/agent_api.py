from fastapi import APIRouter
from app.models.agent_request import AgentRequest
from app.models.agent_response import AgentResponse
from app.models.user_info import UserInfo
from app.services.agent_service import AgentService

router = APIRouter()
agent_service = AgentService()

@router.post("/query", response_model=AgentResponse)
async def handle_query(request: AgentRequest):
    user_info = UserInfo(
        user_id=request.user_id,
        user_name=request.user_name
    )

    response = await agent_service.handle_request(request.user_input, user_info)
    return AgentResponse(result=response)