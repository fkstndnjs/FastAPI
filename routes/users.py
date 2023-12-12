from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import select

from database.connection import get_session
from models.users import User, TokenResponse

user_router = APIRouter(tags=["User"])

# 사용자 등록 엔드포인트
@user_router.post("/signup")
async def sign_user_up(user: User, session=Depends(get_session)) -> dict:
    # 이메일을 기준으로 기존 사용자 존재 여부를 확인합니다.
    statement = select(User).where(User.email == user.email)
    user_exist = session.exec(statement).first()

    if user_exist:
        # 이미 존재하는 사용자의 경우, 오류를 반환합니다.
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with email provided exists")

    session.add(user)  # 새 사용자를 데이터베이스에 추가합니다.
    session.commit()  # 데이터베이스 변경사항을 커밋합니다.

    return {"message": "User created successfully"}

# 사용자 로그인 엔드포인트
@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(
        session=Depends(get_session)) -> dict:
    
    # 이메일을 기준으로 사용자 존재 여부를 확인합니다.
    statement = select(User).where(User.email == user.username)
    user_exist = session.exec(statement).first()
    if not user_exist:
        # 존재하지 않는 사용자의 경우, 오류를 반환합니다.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist."
        )
    
    # 사용자 비밀번호가 일치하는지 확인합니다.
    if user.password == user_exist.password:
        # JWT 액세스 토큰을 생성하고 반환합니다. (여기서는 단순 문자열 "success"를 사용합니다)
        access_token = "success"
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

    # 비밀번호가 일치하지 않는 경우, 오류를 반환합니다.
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )
