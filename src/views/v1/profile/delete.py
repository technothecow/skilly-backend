from fastapi import APIRouter, Response, status, Depends
from typing import Annotated

from src.models.profile import UserProfile, get_profile
from src.models.redirect import Redirect
from src.oauth2.oauth2 import remove_auth_cookies
from src.s3.s3 import get_s3, S3

router = APIRouter(prefix='/v1/profile')


@router.delete('')
async def v1_profile_delete(
        response: Response,
        profile: Annotated[UserProfile, Depends(get_profile)],
        s3: Annotated[S3, Depends(get_s3)]
) -> Redirect:
    remove_auth_cookies(response)
    await profile.delete()
    await s3.delete_object(f'{profile.username}.jpeg')
    return Redirect(redirect='/')
