from typing import List

from fastapi import APIRouter, status

from model.answer import Answer
from model.answer_update_request import AnswerUpdateRequest
from service import answer_service

router: APIRouter = APIRouter(prefix="/answer", tags=["answer"])


@router.post("/", response_model=Answer, status_code=status.HTTP_201_CREATED)
async def create_answer(answer: Answer) -> Answer:
    return await answer_service.create_answer(answer)


@router.get("/", response_model=List[Answer], status_code=status.HTTP_200_OK)
async def get_all_answers() -> List[Answer]:
    return await answer_service.get_all_answers()


@router.get("/{answer_id}", response_model=Answer, status_code=status.HTTP_200_OK)
async def get_answer_by_id(answer_id: int) -> Answer:
    return await answer_service.get_answer_by_id(answer_id)


@router.put("/{answer_id}", response_model=Answer, status_code=status.HTTP_200_OK)
async def update_answer(answer_id: int, answer_update_request: AnswerUpdateRequest) -> Answer:
    return await answer_service.update_answer(answer_id, answer_update_request.selected_option)


@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer_by_id(answer_id: int) -> None:
    await answer_service.delete_answer_by_id(answer_id)