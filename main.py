from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from database.connection import conn
from routes.events import event_router
from routes.users import user_router
import uvicorn

app = FastAPI()

app.include_router(event_router, prefix="/event")  # Service Path: "/event/*"
app.include_router(user_router, prefix="/user")  # Service Path: "/event/*"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.on_event("startup")  # Creates DB Connection and Tables on Startup
def on_startup():
    conn()


if __name__ == "__main__":  # Runs uvicorn Server on Startup as Main Module
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
