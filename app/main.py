from fastapi import FastAPI

app = FastAPI(title="AI Agent Reservation Service (Gemini 기반)")

@app.get("/healthz")
def health_check():
    return {"status": "ok"}
