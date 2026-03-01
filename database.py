""" 
# ! Sync DATABASE
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from app.utils.settings import settings


print("DB_CONNECTION:", settings.DB_CONNECTION)
engine = create_engine(settings.DB_CONNECTION)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        print("Database session created successfully.")
        yield db
    finally:
        db.close() 
"""


# ! Async DATABASE
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.utils.settings import settings

print("DB_CONNECTION:", settings.DB_CONNECTION)
engine = create_async_engine(settings.DB_CONNECTION, echo=False)
print("Connection with database established.")

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            # print("Database session created successfully.")
            yield db
        finally:
            await db.close()