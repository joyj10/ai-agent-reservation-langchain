import pytest
from app.agents.agent import ReservationAgent
from app.models.user_info import UserInfo
from app.memory.user_memory import get_user_memory


@pytest.mark.asyncio
async def test_reservation_agent_availability_check():
    agent = ReservationAgent()

    user_info = UserInfo(
        user_id=101,
        name="홍길동",
        contact="010-1234-5678"
    )

    user_input = "7월 1일 15시에 강남 회의실 예약 가능한가요?"

    result = await agent.run(user_input=user_input, user_info=user_info)

    print("\n[예약 가능 여부 확인 응답]\n", result)
    assert "예약 가능" in result or "예약 불가" in result


@pytest.mark.asyncio
async def test_reservation_agent_booking_flow_multiturn():
    agent = ReservationAgent()
    user_id = 102

    user_info = UserInfo(
        user_id=user_id,
        name="춘식",
        contact="010-5678-1234"
    )

    # 멀티턴을 위해 메모리 초기화
    memory = get_user_memory(user_id)
    memory.clear()

    # 1턴: 일부 정보만 입력
    result1 = await agent.run("7월 1일 오후 3시에 예약하고 싶어요", user_info)
    print("\n[1턴 응답]\n", result1)

    # 2턴: 장소 입력
    result2 = await agent.run("강남 회의실 A", user_info)
    print("\n[2턴 응답]\n", result2)

    assert any(phrase in result2 for phrase in ["예약 요청", "예약 완료", "예약을 도와드릴게요"])


@pytest.mark.asyncio
async def test_reservation_agent_faq_response():
    agent = ReservationAgent()

    user_info = UserInfo(
        user_id=103,
        name="라이언",
        contact="010-1111-2222"
    )

    user_input = "예약 취소하면 수수료 있나요?"

    result = await agent.run(user_input=user_input, user_info=user_info)

    print("\n[FAQ 응답]\n", result)
    assert "취소" in result or "수수료" in result
