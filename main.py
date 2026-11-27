from contextlib import asynccontextmanager

from fastapi import FastAPI

from controller.test_controller import router as test_router
from database import database

from controller.question_controller import router as question_router

from controller.answer_controller import router as answer_router

from controller.statistics_controller import router as statistics_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await database.connect()
    print("Database connected")
    yield
    await database.disconnect()
    print("Database disconnected")


app: FastAPI = FastAPI(title="Poll Service", lifespan=lifespan)

app.include_router(test_router)

app.include_router(question_router)

app.include_router(answer_router)

app.include_router(statistics_router)