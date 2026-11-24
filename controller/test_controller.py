from typing import Dict

from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/test", status_code=200)
async def test() -> Dict[str, str]:
    return {"message": "Poll service is working"}
