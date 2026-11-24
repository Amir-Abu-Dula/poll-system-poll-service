from typing import Optional

import httpx
from fastapi import HTTPException, status

from api.internal_api.user_service.model.user_response import UserResponse
from database import config


async def get_user_by_id(user_id: int) -> Optional[UserResponse]:
    url: str = f"{config.USER_SERVICE_BASE_URL}/user/{user_id}"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User service is unavailable"
        )

    if response.status_code == status.HTTP_404_NOT_FOUND:
        return None

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unexpected response from the user service"
        )

    return UserResponse(**response.json())