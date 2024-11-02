from typing import Annotated
from fastapi import APIRouter, Response, Depends

from src.models.errors import Error
from src.models.profile import UserProfile, get_profile

router = APIRouter(prefix='/v1/profile')


@router.get('')
async def v1_profile_get(
        response: Response,
        profile: Annotated[UserProfile, Depends(get_profile)]
) -> UserProfile | Error:
    if not profile:
        response.status_code = 404
        return Error(message='User not found')
    return profile
