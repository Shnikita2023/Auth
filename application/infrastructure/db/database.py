import redis.asyncio as redis
from redis.asyncio import ConnectionPool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from application.config import settings

DATABASE_URL: str = settings.db.database_url_asyncpg
REDIS_URL: str = settings.redis.url

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

pool_redis: ConnectionPool = redis.ConnectionPool.from_url(url=REDIS_URL)

