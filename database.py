from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///app.db"

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
