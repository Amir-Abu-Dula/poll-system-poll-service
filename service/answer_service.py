from typing import List, Optional

from fastapi import HTTPException, status

from model.answer import Answer, SelectedOption
from repository import answer_repository
from service import question_service


async def create_answer(answer: Answer) -> Answer:
    await question_service.get_question_by_id(answer.question_id)

    existing_answer: Optional[Answer] = await answer_repository.get_answer_by_user_and_question(
        answer.user_id, answer.question_id
    )
    if existing_answer is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"User with id {answer.user_id} has already answered question "
                f"with id {answer.question_id}. Use the update endpoint to change it."
            )
        )

    new_answer_id: int = await answer_repository.create_answer(answer)
    created_answer: Optional[Answer] = await answer_repository.get_answer_by_id(new_answer_id)
    if created_answer is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Answer was created but could not be read back"
        )
    return created_answer


async def get_answer_by_id(answer_id: int) -> Answer:
    answer: Optional[Answer] = await answer_repository.get_answer_by_id(answer_id)
    if answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Answer with id {answer_id} not found"
        )
    return answer


async def get_all_answers() -> List[Answer]:
    return await answer_repository.get_all_answers()


async def update_answer(answer_id: int, selected_option: SelectedOption) -> Answer:
    await get_answer_by_id(answer_id)

    updated_answer: Optional[Answer] = await answer_repository.update_answer(answer_id, selected_option)
    if updated_answer is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Answer was updated but could not be read back"
        )
    return updated_answer


async def delete_answer_by_id(answer_id: int) -> None:
    await get_answer_by_id(answer_id)
    await answer_repository.delete_answer_by_id(answer_id)