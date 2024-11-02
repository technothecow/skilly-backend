from typing import Annotated
from fastapi import APIRouter, Depends, Response, status, UploadFile, File

from src.models.errors import Error
from src.models.profile import UserProfile, get_profile
from src.s3.s3 import S3

router = APIRouter(prefix='/v1/profile/picture')


@router.post('')
async def v1_profile_picture_post(
        response: Response,
        profile: Annotated[UserProfile, Depends(get_profile)],
        picture: UploadFile = File(...)
) -> None | Error:
    if not profile:
        response.status_code = status.HTTP_404_NOT_FOUND
        return Error(message='User not found')

    username = profile.username
    s3 = S3()

    await s3.send_object(f'{username}.jpeg', await picture.read(), content_type='image/jpeg')
