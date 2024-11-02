from fastapi import APIRouter, Response, Depends
from typing import Annotated

from src.models.errors import Error
from src.models.profile import UserProfile, get_profile

router = APIRouter(prefix='/v1/profile')


@router.post('')
async def v1_profile_post(
        response: Response,
        new_profile: UserProfile,
        old_profile: Annotated[UserProfile, Depends(get_profile)]
) -> UserProfile | Error:
    if not old_profile:
        response.status_code = 404
        return Error(message='User not found')

    if new_profile.username != old_profile.username:
        response.status_code = 400
        return Error(message='Username cannot be changed')

    old_profile.update(new_profile)
    await old_profile.apply()

    return old_profile
