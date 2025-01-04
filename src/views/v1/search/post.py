import logging
from fastapi import APIRouter, Depends
from typing import Annotated

from src.db.db import MongoDB
from src.models.search import SearchRequest, UserSearchData, SearchData
from src.oauth2.oauth2 import oauth2_scheme

router = APIRouter(prefix='/v1/search')


@router.post('')
async def v1_search_post(body: SearchRequest, token: Annotated[str, Depends(oauth2_scheme)]) -> SearchData:
    logger = logging.getLogger(__name__)

    username_substring = body.username
    learn_categories = body.learn_categories
    teach_categories = body.teach_categories
    page = body.page

    cursor = MongoDB()

    users = []
    async for user in cursor.collection.find({
        'username': {'$regex': f'.*{username_substring}.*'},
        'learn_categories': {'$all': learn_categories} if learn_categories else {'$exists': True},
        'teach_categories': {'$all': teach_categories} if teach_categories else {'$exists': True}
    }).skip((page - 1) * 10).limit(10).sort('username', 1 if username_substring else 1):
        users.append(UserSearchData(username=user['username'], display_name=user['display_name'],
                                    description=user['description'], learn_categories=user['learn_categories'],
                                    teach_categories=user['teach_categories']))

    return SearchData(users=users)
