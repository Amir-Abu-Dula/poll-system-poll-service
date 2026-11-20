from contextlib import asynccontextmanager

from fastapi import FastAPI

from controller.test_controller import router as test_router
from database import database


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await database.connect()
    print("Database connected")
    yield
    await database.disconnect()
    print("Database disconnected")


app: FastAPI = FastAPI(title="Poll Service", lifespan=lifespan)

app.include_router(test_router)