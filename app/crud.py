from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import User
from .schemas import UserCreate
from .auth import get_password_hash

async def create_user(session: AsyncSession, user_in: UserCreate):
    db_user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password),mobile_number=user_in.mobile_number)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

async def get_user_by_email(session: AsyncSession, email: str):
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_details(session:AsyncSession):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


