from langchain.tools import tool
import httpx

AVAILABILITY_API_URL = "https://your.api/availability"

@tool
async def availability_tool(location: str, date: str, time: str) -> str:
    """
    특정 장소, 날짜, 시간에 예약 가능 여부를 외부 API를 통해 확인합니다.

    Args:
        location (str): 예약하려는 장소 (예: "강남 회의실 A")
        date (str): 예약 날짜 (예: "2025-07-01")
        time (str): 예약 시간 (예: "15:00")

    Returns:
        str: 예약 가능 여부에 대한 안내 문구
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                AVAILABILITY_API_URL,
                params={"location": location, "date": date, "time": time},
                timeout=5.0
            )

        if response.status_code == 200:
            data = response.json()
            is_available = data.get("available", False)

            if is_available:
                return (
                    f"[예약 가능] {date} {time}에 '{location}'은 예약 가능합니다. "
                    f"원하시면 바로 예약을 도와드릴게요!"
                )
            else:
                return (
                    f"[예약 불가] 죄송합니다. {date} {time}에 '{location}'은 이미 예약이 완료되었습니다. "
                    f"다른 시간이나 장소를 원하시나요?"
                )
        else:
            return f"[오류] 예약 가능 여부 확인 중 오류가 발생했습니다. (Status: {response.status_code})"

    except Exception as e:
        return f"[예외 발생] API 호출 중 오류가 발생했습니다: {str(e)}"