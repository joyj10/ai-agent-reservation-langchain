from typing import Optional


async def create_booking(
        name: str,
        date: str,
        time: str,
        location: str,
        contact: Optional[str] = None,
        memo: Optional[str] = None
) -> str:
    """
    예약 등록 (POST /api/bookings)
    """
    return (
        "[MOCK 응답] 예약 등록 완료\n"
        f"예약번호: {date}_01\n"
        f"예약자: {name}\n"
        f"일시: {date} {time}\n"
        f"장소: {location}\n"
        f"연락처: {contact or '미입력'}\n"
        f"요청사항: {memo or '없음'}"
    )


async def update_booking(
        reservation_id: str,
        name: str,
        date: str,
        time: str,
        location: str,
        contact: Optional[str] = None,
        memo: Optional[str] = None
) -> str:
    """
    예약 수정 (PATCH /api/bookings/{id})
    """
    if not reservation_id:
        return "[에러] 예약 수정에는 reservation_id가 필요합니다."

    return (
        "[MOCK 응답] 예약 수정 완료\n"
        f"예약 ID: {reservation_id}\n"
        f"예약자: {name}\n"
        f"일시: {date} {time}\n"
        f"장소: {location}\n"
        f"연락처: {contact or '미입력'}\n"
        f"요청사항: {memo or '없음'}"
    )


async def cancel_booking(reservation_id: str) -> str:
    """
    예약 취소 (DELETE /api/bookings/{id})
    """
    if not reservation_id:
        return "[에러] 예약 취소에는 reservation_id가 필요합니다."

    return (
        "[MOCK 응답] 예약 취소 완료\n"
        f"예약 ID: {reservation_id}"
    )
