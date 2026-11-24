from typing import Any, Dict, List, Optional

from databases.interfaces import Record

from database import database
from model.question import Question


def _to_question(record: Record) -> Question:
    return Question(
        id=record["id"],
        title=record["title"],
        first_option=record["first_option"],
        second_option=record["second_option"],
        third_option=record["third_option"],
        fourth_option=record["fourth_option"]
    )


async def create_question(question: Question) -> int:
    query: str = """
    INSERT INTO question (title, first_option, second_option, third_option, fourth_option)
    VALUES (:title, :first_option, :second_option, :third_option, :fourth_option)
    """
    values: Dict[str, Any] = {
        "title": question.title,
        "first_option": question.first_option,
        "second_option": question.second_option,
        "third_option": question.third_option,
        "fourth_option": question.fourth_option
    }
    return await database.execute(query, values)


async def get_question_by_id(question_id: int) -> Optional[Question]:
    query: str = """
    SELECT * FROM question WHERE id = :question_id
    """
    record: Optional[Record] = await database.fetch_one(query, {"question_id": question_id})
    return _to_question(record) if record else None


async def get_all_questions() -> List[Question]:
    query: str = """
    SELECT * FROM question
    """
    records: List[Record] = await database.fetch_all(query)
    return [_to_question(record) for record in records]


async def update_question(question_id: int, question: Question) -> Optional[Question]:
    query: str = """
    UPDATE question
    SET title = :title,
        first_option = :first_option,
        second_option = :second_option,
        third_option = :third_option,
        fourth_option = :fourth_option
    WHERE id = :question_id
    """
    values: Dict[str, Any] = {
        "title": question.title,
        "first_option": question.first_option,
        "second_option": question.second_option,
        "third_option": question.third_option,
        "fourth_option": question.fourth_option,
        "question_id": question_id
    }
    await database.execute(query, values)
    return await get_question_by_id(question_id)


async def delete_question_by_id(question_id: int) -> None:
    query: str = """
    DELETE FROM question WHERE id = :question_id
    """
    await database.execute(query, {"question_id": question_id})