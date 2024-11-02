from fastapi import APIRouter, Response, status

from src.oauth2.oauth2 import remove_auth_cookies

router = APIRouter(prefix='/v1/profile/sign-out')


@router.post('')
async def v1_profile_sign_out_post(response: Response):
    remove_auth_cookies(response)
    return {'redirect': '/login'}
