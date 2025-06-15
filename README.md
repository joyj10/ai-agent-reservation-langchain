# AI 기반 예약 서비스 에이전트
(LangChain 기반 단순 flow 예제 프로젝트)

## 📌 프로젝트 소개

**"ai-agent-reservation-langchain"** 프로젝트는 예약 서비스에서 **자연어 기반 검색 및 요청 처리 기능**을 제공 하는 **LangChain 기반 AI Agent 학습용 예제**이다.

본 프로젝트는 **단순한 flow 예제**를 중심으로 구성되어 있다.


### 목적
- LangChain을 활용한 **AI Agent 구성 패턴** 학습
- RAG 기반 검색 + 예약 처리 flow 구성 예제 구현
- LLM 기반 Intent 분석 → Tool 기반 처리 흐름 체험
- Agent 기반 서비스 구현 시 기본 구조 설계 참고용 예제 제공

**주의: 본 프로젝트는 학습 및 POC(Proof of Concept) 용도로 구성된 단순 flow 예제이며, 엔터프라이즈 프로덕션용 구조는 아니다.**

---

## 🎯 프로젝트 목표

- 본문 및 첨부파일 내용을 벡터화하여 자연어 기반 검색 기능 제공
- 예약 등록, 예약 취소, 예약 수정 기능을 자연어 기반으로 처리
- AI Agent가 사용자의 의도를 파악해 원하는 업무를 처리 flow 구현 
- LangChain 기반 Agent 설계 방법 학습

---

## 📂 프로젝트 구조
```text
ai-agent-reservation-langchain/
├── app/
│   ├── api/                   # API 라우터 구성
│   ├── core/                  # 설정 및 공통 유틸리티
│   ├── models/                # Request/Response 모델 정의
│   ├── services/              # Agent 처리 흐름, Intent 분석 서비스
│   ├── agents/                # AI Agent 구성 (LangChain 기반)
│   │   ├── tools/             # SearchTool, BookingTool, SummarizationTool
│   ├── tests/                 # 테스트 코드
├── .gitignore
├── .env
├── requirements.txt
├── README.md
```

---

## 🛠️ 기술 스택

| 영역                     | 사용 기술                                 |
|--------------------------|---------------------------------------|
| 언어                     | Python 3.12                           |
| 웹 프레임워크            | FastAPI                               |
| AI Agent 프레임워크      | LangChain 기반 커스텀 구성                   |
| 대규모 언어 모델 (LLM)    | Gemini 2.0                            |
| 벡터 검색                | RAG 시스템 (Qdrant 등과 연동)                |
| 환경 구성                | venv + requirements.txt               |
| 배포 환경                | 미구현                                   |
| 상태 관리 (확장 가능)    | Redis 등 활용 가능 (Short-term Memory 구성 시) |


---
## 🤖 이번 프로젝트에 적용한 LLM: Gemini 2.0 Flash

```text
self.llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # 최신 Gemini Flash 모델 (2025 기준)
    temperature=0              # 일관된 결과를 위한 설정
)
```
- gemini-2.0-flash는 Google에서 제공하는 최신 Flash 계열 모델
  - 최대 100만 토큰 context 지원 
  - 응답 속도가 빠르고, 멀티턴 챗봇이나 실시간 처리 서비스에 적합 
  - 비용도 비교적 저렴해서 테스트용/프로토타입에 잘 어울림

- temperature=0은 항상 비슷한 결과를 출력하게 해주는 옵션
  - 테스트 자동화나 의도 분류 같은 결정 기반 로직에는 꼭 필요한 설정 
  - 온도를 높이면 창의적인 응답은 늘지만, 같은 입력에도 결과가 달라질 수 있음 
  - 이번 프로젝트에서는 의도(Intent) 판단 → 툴 선택 흐름이라 0이 안정적임
  - temperature 옵션
    - temperature=0:
      - 응답이 논리적이고 예측 가능 
      - 테스트나 분기 판단에 적합
    - temperature=0.7~1.0:
    - 응답이 자연스럽고 창의적 
    - 글쓰기, 요약, 아이디어 생성 등에 적합




---

## ✨ 주요 기능

### 1. Intent 분석
- 사용자 질의를 분석하여 **검색 요청 / 처리 요청 / 기타 요청**으로 Intent 분류
- Intent 분석 결과에 따라 적절한 Tool 호출 흐름 제어

### 2. RAG 기반 검색
- 벡터화된 본문 및 첨부파일 대상 고도화 검색 지원
- 호텔 정보, 관련 문서, 파일 기반 검색 가능
- 검색 품질 개선을 위한 지속적인 RAG 튜닝 적용

### 3. 예약 처리 요청
- 자연어 기반으로 다음과 같은 예약 기능 제공
    - 예약 등록
    - 예약 취소
    - 예약 수정
- 실제 예약 시스템과 REST API 연동 가능

### 4. 기타 기능
- 예약 요청 요약 기능 제공 (Summarization Tool 활용)
- 향후 멀티턴 흐름, 개인화 기능 확장 가능

---

## 🗺️ 서비스 흐름
```txt
사용자 자연어 질의
    ↓
AI Agent (LLM 기반 Intent 분석)
    ↓
Tool 직접 호출 (구조화된 결과)
    ↓
LLM에 Tool 결과를 Prompt로 전달 → 자연어 응답 구성
    ↓
최종 결과 응답
```

### 단계별 설명
- 사용자 질의
  - 사용자가 자연어로 요청을 입력
  - 예: ‘00호텔’ 정보 검색해줘
- LLM 기반 Intent 분석
  - LLM이 이 질의를 분석해 "검색" 요청임을 판단하고, 내부에 연결된 search_tool 을 호출해야 한다고 결정
- Tool 직접 호출
  - Agent는 판단된 결과에 따라 직접 search_tool(keyword=’00호텔’) 같은 형식으로 내부 메서드를 호출
  구조화된 데이터 형태로 반환
- LLM을 활용한 결과 응답 구성
  - 구조화된 데이터 결과를 별도의 LLM Prompt 통해 자연어로 변환
- 결과 응답
  - LLM이 구성한 자연어 응답을 사용자에게 전달
  - 예: 00호텔 관련 문서는 3건 입니다. 제목: 00호텔 객실…


---

## 🚀 실행 방법

```bash
# 가상환경 구성
python -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# FastAPI 서버 실행
uvicorn app.main:app --reload --port 8000

# 테스트 예시
curl -X POST http://localhost:8000/agent/query \
     -H "Content-Type: application/json" \
     -d '{"user_input": "AI호텔 객실 관련 문서 보여줘"}'
```

---

## ✨ 주의 사항
본 프로젝트는 학습용으로 구성된 단순 flow 예제이다.
실제 운영 서비스 구축 시에는 다음 사항을 추가로 고려해야 한다.
- Tool 호출 오류 처리 및 재시도 로직
- 멀티턴 대화 흐름 관리 (Short-term Memory + chat_history 설계)
- 사용자 인증/권한 검증 처리
- 서비스 모니터링 및 로깅 구성
- Prompt Template 관리 및 버전 관리 체계 구축

📚 참고 자료
- LangChain 공식 문서: https://python.langchain.com
- FastAPI 공식 문서: https://fastapi.tiangolo.com
- Generative AI API 가이드: https://ai.google.dev