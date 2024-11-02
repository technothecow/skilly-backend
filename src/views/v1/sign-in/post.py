from fastapi import APIRouter, Response, status

from src.models.auth import UserAuthentication
from src.models.errors import Error
from src.models.redirect import Redirect
from src.oauth2.oauth2 import authenticate_user, create_access_token, set_auth_cookies

router = APIRouter(prefix='/v1/sign-in')


@router.post('')
async def v1_sign_in_post(response: Response, user: UserAuthentication) -> Error | Redirect:
    user_info = await authenticate_user(user.email, user.password)

    if not user_info:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Error(message='Incorrect email or password')

    access_token = create_access_token(data={"sub": user.email})
    set_auth_cookies(response, access_token)

    if not user_info.get('is_registered'):
        return Redirect(redirect='/profile/fill')

    return Redirect(redirect='/home')
