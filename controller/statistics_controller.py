from typing import List

from fastapi import APIRouter, status

from model.statistics_response import (
    QuestionAnswersCountResponse,
    QuestionResultsResponse,
    UserAnswersCountResponse,
    UserAnswersResponse,
)
from service import statistics_service

router: APIRouter = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/questions", response_model=List[QuestionResultsResponse], status_code=status.HTTP_200_OK)
async def get_all_questions_results() -> List[QuestionResultsResponse]:
    return await statistics_service.get_all_questions_results()


@router.get("/question/{question_id}", response_model=QuestionResultsResponse, status_code=status.HTTP_200_OK)
async def get_question_results(question_id: int) -> QuestionResultsResponse:
    return await statistics_service.get_question_results(question_id)


@router.get("/question/{question_id}/count", response_model=QuestionAnswersCountResponse, status_code=status.HTTP_200_OK)
async def get_question_answers_count(question_id: int) -> QuestionAnswersCountResponse:
    return await statistics_service.get_question_answers_count(question_id)


@router.get("/user/{user_id}", response_model=UserAnswersResponse, status_code=status.HTTP_200_OK)
async def get_user_answers(user_id: int) -> UserAnswersResponse:
    return await statistics_service.get_user_answers(user_id)


@router.get("/user/{user_id}/count", response_model=UserAnswersCountResponse, status_code=status.HTTP_200_OK)
async def get_user_answers_count(user_id: int) -> UserAnswersCountResponse:
    return await statistics_service.get_user_answers_count(user_id)