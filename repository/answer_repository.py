from typing import Any, Dict, List, Optional

from databases.interfaces import Record

from database import database
from model.answer import Answer, SelectedOption


def _to_answer(record: Record) -> Answer:
    return Answer(
        id=record["id"],
        question_id=record["question_id"],
        user_id=record["user_id"],
        selected_option=record["selected_option"]
    )


async def create_answer(answer: Answer) -> int:
    query: str = """
    INSERT INTO answer (question_id, user_id, selected_option)
    VALUES (:question_id, :user_id, :selected_option)
    """
    values: Dict[str, Any] = {
        "question_id": answer.question_id,
        "user_id": answer.user_id,
        "selected_option": answer.selected_option.name
    }
    return await database.execute(query, values)


async def get_answer_by_id(answer_id: int) -> Optional[Answer]:
    query: str = """
    SELECT * FROM answer WHERE id = :answer_id
    """
    record: Optional[Record] = await database.fetch_one(query, {"answer_id": answer_id})
    return _to_answer(record) if record else None


async def get_answer_by_user_and_question(user_id: int, question_id: int) -> Optional[Answer]:
    query: str = """
    SELECT * FROM answer
    WHERE user_id = :user_id AND question_id = :question_id
    """
    values: Dict[str, int] = {"user_id": user_id, "question_id": question_id}
    record: Optional[Record] = await database.fetch_one(query, values)
    return _to_answer(record) if record else None


async def get_all_answers() -> List[Answer]:
    query: str = """
    SELECT * FROM answer
    """
    records: List[Record] = await database.fetch_all(query)
    return [_to_answer(record) for record in records]


async def update_answer(answer_id: int, selected_option: SelectedOption) -> Optional[Answer]:
    query: str = """
    UPDATE answer
    SET selected_option = :selected_option
    WHERE id = :answer_id
    """
    values: Dict[str, Any] = {
        "selected_option": selected_option.name,
        "answer_id": answer_id
    }
    await database.execute(query, values)
    return await get_answer_by_id(answer_id)


async def count_answers_by_question_id(question_id: int) -> int:
    query: str = """
    SELECT COUNT(*) AS total FROM answer WHERE question_id = :question_id
    """
    record: Optional[Record] = await database.fetch_one(query, {"question_id": question_id})
    return record["total"] if record else 0


async def delete_answer_by_id(answer_id: int) -> None:
    query: str = """
    DELETE FROM answer WHERE id = :answer_id
    """
    await database.execute(query, {"answer_id": answer_id})

async def delete_answers_by_user_id(user_id: int) -> None:
    query: str = """
    DELETE FROM answer WHERE user_id = :user_id
    """
    await database.execute(query, {"user_id": user_id})