from fastapi import APIRouter
from app.models.agent_request import AgentRequest
from app.models.agent_response import AgentResponse
from app.services.agent_service import AgentService

router = APIRouter()
agent_service = AgentService()

@router.post("/query", response_model=AgentResponse)
async def handle_query(request: AgentRequest):
    response = await agent_service.handle_request(request.user_input)
    return AgentResponse(result=response)