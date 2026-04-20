"""
Creates all database tables from SQLAlchemy models.
Run once after the PostgreSQL container is healthy.
"""

import asyncio
import sys
from pathlib import Path

# Allow running from project root without installing the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from db.models import Base
from db.session import engine


async def init() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.")


if __name__ == "__main__":
    asyncio.run(init())
