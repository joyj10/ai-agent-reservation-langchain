from typing import Optional

from langchain.tools import tool

from app.agents.tools.booking_api_client import create_booking, update_booking, cancel_booking
from app.core.logger import logger

# Mock DB 예시 (실제 환경에서는 외부 DB나 서비스에서 조회)
from app.agents.tools.mock_reservation_db import mock_reservation_db


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
    reservation_id: 예약 ID (수정/취소 시 필요)
    contact: 연락처
    memo: 기타 메모
    """

    logger.debug(f"[booking_tool] action={action}, name={name}, date={date}, time={time}, location={location}, "
                 f"reservation_id={reservation_id}, contact={contact}, memo={memo}")

    try:
        if action == "create":
            # 예약 등록 시, 동일한 이름 + 연락처의 예약이 있는지 확인
            for r_id, resv in mock_reservation_db.items():
                if resv["name"] == name and resv["contact"] == contact:
                    return f"[에러] 이미 등록된 예약자입니다. (예약 ID: {r_id})"

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

            origin = mock_reservation_db.get(reservation_id)
            if not origin:
                return f"[에러] 예약 ID '{reservation_id}'에 해당하는 예약이 존재하지 않습니다."
            if origin["name"] != name or origin["contact"] != contact:
                return "[에러] 예약 수정 권한이 없습니다. 이름 또는 연락처가 일치하지 않습니다."

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

            origin = mock_reservation_db.get(reservation_id)
            if not origin:
                return f"[에러] 예약 ID '{reservation_id}'에 해당하는 예약이 존재하지 않습니다."
            if origin["name"] != name or origin["contact"] != contact:
                return "[에러] 예약 취소 권한이 없습니다. 이름 또는 연락처가 일치하지 않습니다."

            return await cancel_booking(reservation_id)

        else:
            return "[에러] 알 수 없는 action입니다. (create/update/cancel 중 하나여야 함)"

    except Exception as e:
        logger.exception("[booking_tool] 예외 발생")
        return f"[에러] 처리 중 문제가 발생했습니다: {e}"