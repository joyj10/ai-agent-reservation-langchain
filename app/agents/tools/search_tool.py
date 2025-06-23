from langchain.tools import tool
import asyncio
from app.agents.tools.search_api_client import search_place


@tool
def search_tool(query: str) -> str:
    """
    장소 또는 예약 가능한 정보를 검색하는 도구입니다.

    사용자는 특정 장소나 지역에 대한 예약 가능 여부를 물어볼 수 있으며,
    이 툴은 그런 요청을 처리하는 데 사용됩니다.

    사용 예:
    - "서울 강남 호텔 알려줘"
    - "다음 주에 사용할 수 있는 회의실 있나 찾아줘"
    - "오늘 저녁에 예약할 수 있는 레스토랑 검색해줘"

    입력: 자연어 형식의 검색 요청
    출력: 검색 결과에 대한 요약 응답
    """
    try:
        return asyncio.run(search_place(query))
    except Exception as e:
        return f"[에러] 처리 중 문제가 발생했습니다: {e}"