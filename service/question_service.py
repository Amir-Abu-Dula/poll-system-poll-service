from typing import List, Optional

from fastapi import HTTPException, status

from model.question import Question
from repository import answer_repository, question_repository


async def create_question(question: Question) -> Question:
    new_question_id: int = await question_repository.create_question(question)
    created_question: Optional[Question] = await question_repository.get_question_by_id(new_question_id)
    if created_question is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Question was created but could not be read back"
        )
    return created_question


async def get_question_by_id(question_id: int) -> Question:
    question: Optional[Question] = await question_repository.get_question_by_id(question_id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id {question_id} not found"
        )
    return question


async def get_all_questions() -> List[Question]:
    return await question_repository.get_all_questions()


async def update_question(question_id: int, question: Question) -> Question:
    await get_question_by_id(question_id)

    answers_count: int = await answer_repository.count_answers_by_question_id(question_id)
    if answers_count > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Question with id {question_id} cannot be updated "
                f"because it already has {answers_count} answers"
            )
        )

    updated_question: Optional[Question] = await question_repository.update_question(question_id, question)
    if updated_question is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Question was updated but could not be read back"
        )
    return updated_question


async def delete_question_by_id(question_id: int) -> None:
    await get_question_by_id(question_id)
    await question_repository.delete_question_by_id(question_id)