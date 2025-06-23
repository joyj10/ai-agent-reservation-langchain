from typing import Optional

from langchain.tools import tool

from app.agents.tools.booking_api_client import create_booking, update_booking, cancel_booking
from app.core.logger import logger


@tool
async def booking_tool(
        action: str,
        name: Optional[str] = None,
        date: Optional[str] = None,
        time: Optional[str] = None,
        location: Optional[str] = None,
        reservation_id: Optional[str] = None,
        contact: Optional[str] = None,
        memo: Optional[str] = None,
) -> str:
    """
   장소 예약, 예약 수정, 예약 취소를 처리하는 도구입니다.
   action: 'create', 'update', 'cancel' 중 하나
   name: 예약자 이름
   date: 예약 날짜 (YYYY-MM-DD)
   time: 예약 시간 (HH:MM)
   location: 장소 이름
   reservation_id: 예약 ID (수정/취소/조회 시 필요)
   contact: 연락처
   memo: 기타 메모
   """
    # 디버깅용
    print(
        f"[booking_tool] action={action}, name={name}, date={date}, time={time}, "
        f"location={location}, reservation_id={reservation_id}, contact={contact}, memo={memo}"
    )

    params = {k: v for k, v in locals().items() if k != "self"}
    logger.debug(f"[booking_tool] 파라미터: {params}")

    try:
        if action == "create":
            if not (name and date and time and location):
                return "[에러] 예약 생성에는 이름, 날짜, 시간, 장소가 모두 필요합니다."
            return await create_booking(
                name=name,
                date=date,
                time=time,
                location=location,
                contact=contact,
                memo=memo,
            )
        elif action == "update":
            if not (reservation_id and name and date and time and location):
                return "[에러] 예약 수정에는 예약 ID, 이름, 날짜, 시간, 장소가 모두 필요합니다."
            return await update_booking(
                reservation_id=reservation_id,
                name=name,
                date=date,
                time=time,
                location=location,
                contact=contact,
                memo=memo,
            )
        elif action == "cancel":
            if not reservation_id:
                return "[에러] 예약 취소에는 예약 ID가 필요합니다."
            return await cancel_booking(reservation_id)
        else:
            return "[에러] 알 수 없는 action입니다. (create/update/cancel 중 하나여야 함)"
    except Exception as e:
        return f"[에러] 처리 중 문제가 발생했습니다: {e}"