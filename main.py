from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import conn
from routes.events import event_router
from routes.users import user_router
import uvicorn

app = FastAPI()

# 이벤트 관련 경로를 애플리케이션에 포함시킵니다. 서비스 경로: "/event/*"
app.include_router(event_router, prefix="/event")

# 사용자 관련 경로를 애플리케이션에 포함시킵니다. 서비스 경로: "/user/*"
app.include_router(user_router, prefix="/user")

# CORS 미들웨어를 추가합니다. 이를 통해 모든 도메인, HTTP 메소드, 헤더가 허용됩니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 서버가 시작될 때 데이터베이스 연결을 설정합니다.
@app.on_event("startup")  # 스타트업 이벤트 시 데이터베이스 연결 및 테이블 생성
def on_startup():
    conn()

# 메인 모듈로서 uvicorn 서버를 실행합니다. 주소는 "127.0.0.1"이며, 포트는 8000입니다.
if __name__ == "__main__":  # 메인 모듈로 실행 시 uvicorn 서버 시작
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
