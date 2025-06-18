import re
import asyncio
from datetime import datetime, timedelta
from typing import Optional

from langchain.tools import tool  # 사용하는 프레임워크에 맞게 수정

from app.agents.tools.booking_api_client import create_booking, update_booking, cancel_booking


@tool
def booking_tool(query: str) -> str:
    """
    장소 예약 요청, 수정, 취소를 처리하는 도구입니다.
    """
    try:
        intent = detect_intent(query)

        if intent == "create":
            parsed = parse_query(query)
            if not parsed:
                return "[에러] 예약 정보를 충분히 이해하지 못했습니다."

            return asyncio.run(create_booking(
                name="홍길동",
                date=parsed["date"],
                time=parsed["time"],
                location=parsed["location"],
                contact=parsed.get("contact"),
                memo=parsed.get("memo"),
            ))

        elif intent == "update":
            parsed = parse_query(query)
            if not parsed or not parsed.get("reservation_id"):
                return "[에러] 수정하려면 예약 ID와 새 정보가 필요합니다."

            return asyncio.run(update_booking(
                reservation_id=parsed["reservation_id"],
                name="홍길동",
                date=parsed["date"],
                time=parsed["time"],
                location=parsed["location"],
                contact=parsed.get("contact"),
                memo=parsed.get("memo"),
            ))

        elif intent == "cancel":
            reservation_id = extract_reservation_id(query)
            if not reservation_id:
                return "[에러] 예약 취소에는 예약 ID가 필요합니다."

            return asyncio.run(cancel_booking(reservation_id))

        else:
            return "[에러] 요청이 예약, 수정, 취소 중 무엇인지 판단할 수 없습니다."

    except Exception as e:
        return f"[에러] 처리 중 문제가 발생했습니다: {e}"


def detect_intent(query: str) -> str:
    """
    자연어에서 예약 intent (create, update, cancel) 추출
    """
    if any(word in query for word in ["예약해", "예약하고", "예약해줘", "예약을 원해"]):
        return "create"
    elif any(word in query for word in ["수정", "변경"]):
        return "update"
    elif any(word in query for word in ["취소", "캔슬"]):
        return "cancel"
    return "unknown"


def parse_query(query: str) -> Optional[dict]:
    """
    간단한 파싱으로 예약 정보 추출 (수정/생성 공통)
    """
    now = datetime.now()
    date = None
    if "오늘" in query:
        date = now.strftime("%Y-%m-%d")
    elif "내일" in query:
        date = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    elif "모레" in query:
        date = (now + timedelta(days=2)).strftime("%Y-%m-%d")
    elif "이번 주말" in query:
        days_ahead = 5 - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        date = (now + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

    time_match = re.search(r"(오전|오후)?\s?(\d{1,2})시", query)
    time = None
    if time_match:
        hour = int(time_match.group(2))
        if time_match.group(1) == "오후" and hour < 12:
            hour += 12
        time = f"{hour:02}:00"

    loc_match = re.search(r"(회의실|카페|호텔|장소)[^\s]*", query)
    location = loc_match.group(0) if loc_match else None

    reservation_id = extract_reservation_id(query)

    if date and time and location:
        return {
            "date": date,
            "time": time,
            "location": location,
            "contact": None,
            "memo": query,
            "reservation_id": reservation_id,
        }
    return None


def extract_reservation_id(query: str) -> Optional[str]:
    """
    쿼리에서 예약 ID 추출 (예: '예약 ID 1234' 형식)
    """
    match = re.search(r"(예약\s*ID[:\s]?)(\w+)", query)
    return match.group(2) if match else None