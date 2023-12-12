from typing import Optional, List
from sqlmodel import JSON, SQLModel, Field, Column
from pydantic import EmailStr

# 이벤트 테이블 모델을 정의합니다. SQLModel을 상속받아 테이블로 사용될 수 있게 합니다.
class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # 이벤트의 고유 ID, 기본키로 선언됩니다.
    title: str  # 이벤트 제목
    image: str  # 이벤트 이미지 URL 또는 경로
    description: str  # 이벤트 설명
    location: str  # 이벤트 장소
    tags: List[str] = Field(sa_column=Column(JSON))  # 이벤트 태그, JSON 컬럼 타입을 사용합니다.

    class Config:
        arbitrary_types_allowed = True  # Pydantic이 아닌 필드 타입을 허용합니다.

# 이벤트 업데이트 요청 메시지 바디를 정의합니다.
class EventUpdate(SQLModel):
    title: Optional[str]  # 선택적으로 업데이트할 이벤트 제목
    image: Optional[str]  # 선택적으로 업데이트할 이벤트 이미지
    description: Optional[str]  # 선택적으로 업데이트할 이벤트 설명
    location: Optional[str]  # 선택적으로 업데이트할 이벤트 장소
    tags: Optional[List[str]]  # 선택적으로 업데이트할 이벤트 태그
