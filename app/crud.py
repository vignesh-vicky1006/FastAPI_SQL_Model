from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from .models import User,RoleMaster,Rolemapping
from .schemas import UserCreate,RolemasterCrete
from .auth import get_password_hash
from fastapi import HTTPException

async def create_user(session: AsyncSession, user_in: UserCreate):
    
    db_user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password),mobile_number=user_in.mobile_number)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    # Create role mapping
    for role_name in user_in.role:
        role_result = await session.execute(
            select(RoleMaster).where(RoleMaster.name == role_name)
        )
        role = role_result.scalar_one_or_none()

        if not role:
            raise HTTPException(status_code=400, detail="Invalid role name")
        
        db_rolemap = Rolemapping(user_id=db_user.id, rolemaster_id=role.id)
        session.add(db_rolemap)
        
    await session.commit()
    return db_user

async def get_user_by_email(session: AsyncSession, email: str):
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_details(session:AsyncSession):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

async def create_rolemaster(session:AsyncSession,role:RolemasterCrete):
    db_role = RoleMaster(name=role.name,description=role.description)
    session.add(db_role)
    await session.commit()
    await session.refresh(db_role)
    return db_role

async def userroles_read(session:AsyncSession,user:int):
    user_role = await session.execute(
        select(Rolemapping).where(Rolemapping.user_id==user).options(
            selectinload(Rolemapping.user),selectinload(Rolemapping.rolemaster)
        )
    )

    result = user_role.scalars().all()
    return result
    
