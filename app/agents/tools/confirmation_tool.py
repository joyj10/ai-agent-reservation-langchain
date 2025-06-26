from langchain.tools import tool
import httpx

CONFIRMATION_API_URL = "https://your.api/reservations/{reservation_id}"

@tool
async def confirmation_tool(reservation_id: str) -> str:
    """
    예약 번호로 예약 상세 정보를 외부 API에서 조회합니다.

    Args:
        reservation_id (str): 예약 ID

    Returns:
        str: 예약 상세 정보 (혹은 오류 메시지)
    """
    url = CONFIRMATION_API_URL.format(reservation_id=reservation_id)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)

        if response.status_code == 200:
            data = response.json()
            return (
                f"[예약 확인]\n"
                f"- 예약 ID: {reservation_id}\n"
                f"- 예약자: {data.get('name')}\n"
                f"- 장소: {data.get('location')}\n"
                f"- 날짜: {data.get('date')}\n"
                f"- 시간: {data.get('time')}\n"
                f"- 상태: {data.get('status')}"
            )
        else:
            return f"[오류] 예약 ID {reservation_id} 조회에 실패했습니다. (Status: {response.status_code})"
    except Exception as e:
        return f"[예외 발생] 예약 확인 중 오류가 발생했습니다: {str(e)}"