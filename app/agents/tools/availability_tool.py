from langchain.tools import tool
from app.agents.tools.mock_reservation_db import mock_reservation_db


@tool
async def availability_tool(location: str, date: str, time: str) -> str:
    """
    특정 장소, 날짜, 시간에 예약 가능 여부를 mock DB를 통해 확인합니다.

    Args:
        location (str): 예약하려는 장소 (예: "강남 회의실 A")
        date (str): 예약 날짜 (예: "2025-07-01")
        time (str): 예약 시간 (예: "15:00")

    Returns:
        str: 예약 가능 여부에 대한 안내 문구
    """
    try:
        for res in mock_reservation_db.values():
            if (
                    res["location"] == location and
                    res["date"] == date and
                    res["time"] == time and
                    res.get("status", "예약됨") != "취소됨"
            ):
                return (
                    f"[예약 불가] 죄송합니다. {date} {time}에 '{location}'은 이미 예약이 완료되었습니다. "
                    f"다른 시간이나 장소를 원하시나요?"
                )

        return (
            f"[예약 가능] {date} {time}에 '{location}'은 예약 가능합니다. "
            f"원하시면 바로 예약을 도와드릴게요!"
        )

    except Exception as e:
        return f"[예외 발생] 예약 가능 여부 확인 중 오류가 발생했습니다: {str(e)}"
