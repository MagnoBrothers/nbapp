from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core import config

settings = config.get_settings()


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True,
    # pool_size=100,
    # max_overflow=100,
    poolclass=NullPool,  # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#using-multiple-asyncio-event-loops
)


async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def close_engine():
    await engine.dispose()


async def get_db() -> AsyncSession:
    """
    Creates the actual session/transaction. We're doing two things in a single context
    manager:
        - create a session
        - create a transaction

    It is equivalent to:
    ```
        async with async_session() as session:
            async with session.begin():
                yield session
    ```

    Nested transaction may be created with:
    ```
        with session.begin_nested() as nested:  # BEGIN SAVEPOINT
            nested.add(some_object)
            nested.rollback()  # ROLLBACK TO SAVEPOINT
    ```
    """
    # async with async_session_factory.begin() as session:
    async with async_session_factory() as session:
        # ... setup
        yield session
        # ... teardown


def get_scoped_session():
    AsyncScopedSession = async_scoped_session(
        async_session_factory, scopefunc=current_task
    )
    return AsyncScopedSession
