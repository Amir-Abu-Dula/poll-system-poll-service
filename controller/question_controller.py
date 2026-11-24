from typing import List

from fastapi import APIRouter, status

from model.question import Question
from service import question_service

router: APIRouter = APIRouter(prefix="/question", tags=["question"])


@router.post("/", response_model=Question, status_code=status.HTTP_201_CREATED)
async def create_question(question: Question) -> Question:
    return await question_service.create_question(question)


@router.get("/", response_model=List[Question], status_code=status.HTTP_200_OK)
async def get_all_questions() -> List[Question]:
    return await question_service.get_all_questions()


@router.get("/{question_id}", response_model=Question, status_code=status.HTTP_200_OK)
async def get_question_by_id(question_id: int) -> Question:
    return await question_service.get_question_by_id(question_id)


@router.put("/{question_id}", response_model=Question, status_code=status.HTTP_200_OK)
async def update_question(question_id: int, question: Question) -> Question:
    return await question_service.update_question(question_id, question)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question_by_id(question_id: int) -> None:
    await question_service.delete_question_by_id(question_id)