from fastapi import APIRouter, Depends, Response, status
from typing import Annotated
from datetime import datetime

from src.models.home import HomeData, RecommendedUser, Chat, Event
from src.oauth2.oauth2 import get_username

router = APIRouter(prefix='/v1/home')


@router.post('')
async def v1_home_post(response: Response, username: Annotated[str, Depends(get_username)]) -> HomeData | dict:
    if not username:
        response.status_code = status.HTTP_307_TEMPORARY_REDIRECT
        return {'redirect': '/profile/fill'}

    # TODO: implement
    return HomeData(
        username=username,
        learn_categories=['Math', 'Science'],
        teach_categories=['Arts', 'Music'],
        recommended=[
            RecommendedUser(
                display_name='John Doe',
                teach_categories=[f'category{i}' for i in range(12)],
                learn_categories=['Arts', 'Music'],
                username='johndoe',
                photo=''
            ),
        ],
        chats=[
            Chat(
                id='1',
                display_name='John Doe',
                username='johndoe',
                last_message='John Doe: Hello',
                status='unread',
                photo=''
            )
        ],
        events=[
            Event(
                name='Math Study Group',
                id='1',
                datetime=datetime.now(),
                description='Join us for a study group on math!'
            )
        ],
        is_maintained=False
    )
