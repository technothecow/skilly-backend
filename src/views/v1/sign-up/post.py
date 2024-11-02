from pydantic import BaseModel
from fastapi import APIRouter, Response, status

from src.models.auth import UserAuthentication
from src.models.errors import Error
from src.models.redirect import Redirect
from src.oauth2.oauth2 import register_user, create_access_token, set_auth_cookies

router = APIRouter(prefix='/v1/sign-up')


@router.post('')
async def v1_sign_up_post(response: Response, user: UserAuthentication) -> Error | Redirect:
    if not await register_user(user.email, user.password):
        response.status_code = status.HTTP_409_CONFLICT
        return Error(message='User with that email already exists')

    access_token = create_access_token(data={"sub": user.email})
    set_auth_cookies(response, access_token)

    return Redirect(redirect='/profile/fill')
