from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from database.connection import get_session
from models.users import User, TokenResponse

user_router = APIRouter(tags=["User"])

@user_router.post("/signup")
async def sign_user_up(user: User, session=Depends(get_session)) -> dict:
    statement = select(User).where(User.email == user.email)
    user_exist = session.exec(statement).first()

    if user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, deatil="User with email provided exists")

    session.add(user)
    session.commit()

    return {"message": "User created successfully"}


@user_router.post("/signin", response_model=TokenResponse)  # Token Response
async def sign_user_in(
        session=Depends(get_session)) -> dict:
    
    # Check If User Exists or Not
    statement = select(User).where(User.email == user.username)
    user_exist = session.exec(statement).first()
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist."
        )
    
    # Verify User Password in the Sign-In Request against Hashed Password
    if user.password == user_exist.password:
        # Creates and Returns JWT Access Token
        access_token = "success"
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

    # Failure to Sign-In: Invalid Password
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed."
    )
