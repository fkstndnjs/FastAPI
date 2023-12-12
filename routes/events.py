from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import select
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List

# 이벤트 관련 API 라우트를 정의합니다. Swagger UI에서 사용할 태그로 "Events"를 지정합니다.
event_router = APIRouter(tags=["Events"])

# 새로운 이벤트를 생성하는 엔드포인트입니다.
@event_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    session.add(new_event)  # 새로운 이벤트를 데이터베이스에 추가합니다.
    session.commit()  # 데이터베이스에 커밋합니다.
    session.refresh(new_event)  # 이벤트 데이터를 새로고침합니다.

    return {
        "message": "Event created successfully."
    }

# 모든 이벤트를 검색하는 엔드포인트입니다.
@event_router.get("/", response_model=List[Event], status_code=status.HTTP_200_OK)
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    statement = select(Event)  # 모든 이벤트 데이터를 선택하는 SQL 문을 생성합니다.
    events = session.exec(statement).all()  # SQL 문을 실행하고 모든 결과를 가져옵니다.

    return events

# 특정 ID를 가진 이벤트를 검색하는 엔드포인트입니다.
@event_router.get("/{id}", response_model=Event, status_code=status.HTTP_200_OK)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)  # 주어진 ID를 가진 이벤트를 검색합니다.
    if event:
        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

# 특정 이벤트를 업데이트하는 엔드포인트입니다.
@event_router.put("/edit/{id}", response_model=Event, status_code=status.HTTP_200_OK)
async def update_event(id: int, new_data: EventUpdate, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)  # 주어진 ID를 가진 이벤트를 검색합니다.
    if event:
        event_data = new_data.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)  # 이벤트 데이터를 업데이트합니다.
        session.add(event)
        session.commit()  # 데이터베이스에 커밋합니다.
        session.refresh(event)  # 이벤트 데이터를 새로고침합니다.

        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )

# 특정 이벤트를 삭제하는 엔드포인트입니다.
@event_router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_event(id: int, session=Depends(get_session)) -> dict:
    event = session.get(Event, id)  # 주어진 ID를 가진 이벤트를 검색합니다.
    if event:
        session.delete(event)  # 이벤트를 삭제합니다.
        session.commit()  # 데이터베이스에 커밋합니다.

        return {
            "message": "Event deleted successfully."
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )
