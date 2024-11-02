from fastapi import APIRouter, Response, status
from fastapi.responses import StreamingResponse

from src.models.errors import Error
from src.s3.s3 import S3

router = APIRouter(prefix='/v1/profile/picture')


@router.get('/{username}')
async def v1_profile_picture_get(response: Response, username: str) -> StreamingResponse:
    s3 = S3()

    image = await s3.get_object(f'{username}.jpeg')

    if image is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return Error(message='Image not found')

    return StreamingResponse(image, media_type='image/jpeg')
