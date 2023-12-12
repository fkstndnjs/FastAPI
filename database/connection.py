from sqlmodel import SQLModel, Session, create_engine
from models.events import Event
from models.users import User

# 데이터베이스 파일 이름과 다이얼렉트를 설정합니다.
filename = "planner.db"
dialect = "sqlite"
db_conn_url = f"{dialect}:///{filename}"
c_args = {"check_same_thread": False}  # SQLite 멀티스레드 문제 해결을 위한 설정

# 데이터베이스 엔진을 생성합니다. echo=True는 SQL 로그를 활성화합니다.
engine = create_engine(db_conn_url, echo=True, connect_args=c_args)

# 데이터베이스 테이블 생성 함수
def conn():
    SQLModel.metadata.create_all(engine)  # 모든 SQLModel 테이블을 생성합니다.

# CRUD 작업을 위한 데이터베이스 세션 생성 함수
def get_session():
    with Session(engine) as session:
        yield session  # 세션을 CRUD 함수에 의존성 주입을 위해 생성합니다.
