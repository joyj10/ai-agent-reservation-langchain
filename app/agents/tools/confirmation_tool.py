from langchain.tools import tool
from app.agents.tools.mock_reservation_db import mock_reservation_db


@tool
async def confirmation_tool(reservation_id: str) -> str:
    """
    예약 번호로 예약 상세 정보를 mock DB에서 조회합니다.

    Args:
        reservation_id (str): 예약 ID

    Returns:
        str: 예약 상세 정보 (혹은 오류 메시지)
    """
    try:
        data = mock_reservation_db.get(reservation_id)

        if not data:
            return f"[오류] 예약 ID {reservation_id}에 해당하는 예약 정보를 찾을 수 없습니다."

        return (
            f"[예약 확인]\n"
            f"- 예약 ID: {reservation_id}\n"
            f"- 예약자: {data.get('name')}\n"
            f"- 장소: {data.get('location')}\n"
            f"- 날짜: {data.get('date')}\n"
            f"- 시간: {data.get('time')}\n"
            f"- 상태: {data.get('status', '예약됨')}"
        )

    except Exception as e:
        return f"[예외 발생] 예약 확인 중 오류가 발생했습니다: {str(e)}"
