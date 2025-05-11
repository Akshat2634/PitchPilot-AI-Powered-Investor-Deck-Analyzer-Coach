from prisma import Prisma
from contextlib import asynccontextmanager

prisma = Prisma()

@asynccontextmanager
async def get_prisma():
    """Context manager to connect to the Prisma database and yield the client."""
    await prisma.connect()
    try:
        yield prisma
    finally:
        await prisma.disconnect()
        