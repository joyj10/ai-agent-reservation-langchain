async def search_place(query: str) -> str:
    """
    장소나 예약 가능한 정보를 검색하는 목(MOCK) API 함수
    실제 API 연동 전 개발 및 테스트용으로 사용
    """
    if "강남" in query:
        return (
            "[MOCK 응답] 검색 결과\n"
            "- 강남역 인근 호텔 A (예약 가능)\n"
            "- 강남 컨퍼런스룸 B (예약 마감)"
        )
    elif "레스토랑" in query or "맛집" in query:
        return (
            "[MOCK 응답] 검색 결과\n"
            "- 이탈리안 레스토랑 Bella\n"
            "- 한식당 맛나당 (잔여석 있음)\n"
            "- 스시 오마카세 카이 (예약 필수)"
        )
    elif "회의실" in query:
        return (
            "[MOCK 응답] 검색 결과\n"
            "- 강서구 비즈니스 센터 2층 회의실 (오전 예약 가능)\n"
            "- 시청역 인근 세미나실 (전일 예약 가능)"
        )
    elif "제주도" in query:
        return (
            "[MOCK 응답] 검색 결과\n"
            "- 제주 중문 리조트 (3박 예약 가능)\n"
            "- 제주 바다 전망 펜션 (2인 가능)"
        )
    elif "호텔" in query:
        return (
            "[MOCK 응답] 검색 결과\n"
            "- 서울 시내 특급 호텔 3곳 (금주 가능)\n"
            "- 부산 해운대 호텔 블루문 (예약 마감)"
        )
    elif "카페" in query:
        return (
            "[MOCK 응답] 검색 결과\n"
            "- 한남동 루프탑 카페 모카 (잔여석 있음)\n"
            "- 이태원 조용한 북카페 (오전만 예약 가능)"
        )
    else:
        return "[MOCK 응답] 관련된 장소를 찾지 못했습니다."