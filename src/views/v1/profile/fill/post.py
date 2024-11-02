from fastapi import Depends, APIRouter, Response, status
from typing import Annotated

from src.models.profile import UserFillProfile, UserProfile, get_profile

router = APIRouter(prefix='/v1/profile/fill')


@router.post('')
async def v1_profile_fill_post(
        response: Response,
        filled_profile: UserFillProfile,
        profile: Annotated[UserProfile, Depends(get_profile)]
):
    if profile.is_registered:
        response.status_code = status.HTTP_307_TEMPORARY_REDIRECT
        return {'redirect': '/home'}

    profile.update(filled_profile)
    await profile.apply()
    return {'redirect': '/home'}
