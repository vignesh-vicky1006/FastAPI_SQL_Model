from fastapi import FastAPI, Depends, HTTPException, status
from app import schemas, crud, auth
from app.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

app = FastAPI()

# REMOVE init_db() -- you're using Alembic now
# @app.on_event("startup")
# async def on_startup():
#     await init_db()

@app.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await auth.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.UserRead)
async def register(user: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    existing = await crud.get_user_by_email(session, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(session, user)

@app.get("/users/me/", response_model=schemas.UserRead)
async def read_users_me(current_user=Depends(auth.get_current_user)):
    return current_user

@app.get("/users/",response_model=List[schemas.UserRead])
async def read_users(db_Session:AsyncSession=Depends(get_session)):
    users= await crud.get_user_details(db_Session)
    return users



# @app.get("/ping")
# async def ping():
#     return {"message": "pong"}
