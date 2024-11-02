from fastapi import APIRouter, Response, status, Depends
from pydantic import BaseModel, Field
from typing import Annotated

from src.config.config import get_config
from src.db.db import MongoDB
from src.models.errors import Error
from src.oauth2.oauth2 import oauth2_scheme

validation_config = get_config().validation_config
router = APIRouter(prefix='/v1/profile/check-username')


class CheckUsernameBody(BaseModel):
    username: str = Field(..., max_length=validation_config.max_name_length)


@router.post('')
async def v1_profile_check_username_post(
        response: Response,
        token: Annotated[str, Depends(oauth2_scheme)],
        body: CheckUsernameBody
) -> Error | None:
    cursor = MongoDB()

    user = await cursor.collection.find_one({'username': body.username})

    if user:
        response.status_code = status.HTTP_409_CONFLICT
        return Error(message='Username already exists')

    return
