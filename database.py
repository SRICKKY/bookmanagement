from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# SQLALCHEMY 
engine = create_async_engine("postgresql+asyncpg://bookmgmt_owner:ZJem9B7jsHAS@ep-autumn-mouse-a1sg9k1r.ap-southeast-1.aws.neon.tech/bookmanagementdb", echo=False)
SessionLocal = async_sessionmaker(engine)

def get_session_local():
    yield SessionLocal()

class Base(DeclarativeBase):
    pass


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()