from typing import Annotated
from fastapi import APIRouter, Depends

from src.oauth2.oauth2 import get_username

router = APIRouter(prefix='/v1/chats')


@router.get('')
async def v1_chats(page: int, username: Annotated[str, Depends(get_username)]):
    if page > 1:
        return {
            'chats': []
        }
    return {
        'chats': [
            {
                'last_message': 'Hello',
                'status': 'unread',
                'username': f'user{page}1',
                'last_action_timestamp': 1111620000000
            },
            {
                'last_message': 'Hi',
                'status': 'read',
                'username': f'user{page}2',
                'last_action_timestamp': 1111620000000
            },
            {
                'last_message': 'Hey',
                'status': 'unread',
                'username': f'user{page}3',
                'last_action_timestamp': 1111620000000
            },
            {
                'last_message': 'Hello',
                'status': 'read',
                'username': f'user{page}4',
                'last_action_timestamp': 1111620000000
            },
            {
                'last_message': 'Hi',
                'status': 'unread',
                'username': f'user{page}5',
                'last_action_timestamp': 1111620000000
            },
            {
                'last_message': 'Hey',
                'status': 'read',
                'username': f'user{page}6',
                'last_action_timestamp': 1111620000000
            },
            {
                'last_message': 'Hello',
                'status': 'unread',
                'username': f'user{page}7',
                'last_action_timestamp': 1111620000000
            },
            {
                'last_message': 'Hi',
                'status': 'read',
                'username': f'user{page}8',
                'last_action_timestamp': 1111620000000
            },
            {
                'last_message': 'Hey',
                'status': 'unread',
                'username': f'user{page}9',
                'last_action_timestamp': 1111620000000
            },
            {
                'last_message': 'Hello',
                'status': 'read',
                'username': f'user{page}10',
                'last_action_timestamp': 1111620000000
            }
        ]
    }
