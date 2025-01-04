from fastapi import APIRouter, Depends, Response
from typing import Annotated

from src.models.search import SearchRequest, UserSearchData, SearchData
from src.oauth2.oauth2 import oauth2_scheme

router = APIRouter(prefix='/v1/search')


@router.post('')
async def v1_search_post(response: Response, body: SearchRequest, token: Annotated[str, Depends(oauth2_scheme)]) -> SearchData:
    # TODO: Implement search logic
    return SearchData(users=[
        UserSearchData(username='test', display_name='Test User', description='This is a test user',
                       learn_categories=['Python', 'FastAPI'], teach_categories=['Python', 'FastAPI']),
    ])