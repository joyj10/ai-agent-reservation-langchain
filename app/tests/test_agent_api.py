import os
import sys

# sys.path 추가로 루트 경로 인식
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_api_booking():
    payload = {
        "user_input": "서울 컨벤션 A홀로 내일 3시 예약 해줘",
        "user_id": 1,
        "name": "wony",
        "contact": "010-1234-1234"
    }
    response = client.post("/agent/query", json=payload)

    print("응답 결과:", response.json())

    assert response.status_code == 200
    assert "result" in response.json()

def test_query_api_search_place():
    payload = {
        "user_input": "강남 호텔 검색해줘",
        "user_id": 1,
        "name": "wony",
        "contact": "010-1234-1234"
    }
    response = client.post("/agent/query", json=payload)

    print("응답 결과:", response.json())

    assert response.status_code == 200
    assert "result" in response.json()


def test_query_api_faq_cancel():
    payload = {
        "user_input": "예약 취소 수수료는 얼마인가요?",
        "user_id": 1,
        "name": "wony",
        "contact": "010-1234-1234"
    }
    response = client.post("/agent/query", json=payload)

    print("응답 결과:", response.json())

    assert response.status_code == 200
    assert "result" in response.json()
    assert "취소" in response.json()["result"] or "수수료" in response.json()["result"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
