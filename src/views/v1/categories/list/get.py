from typing import Annotated
from fastapi import APIRouter, Depends

from src.config.config import get_config
from src.oauth2.oauth2 import oauth2_scheme

router = APIRouter(prefix='/v1/categories/list')


@router.get('')
async def v1_categories_list_get(token: Annotated[str, Depends(oauth2_scheme)]):
    # token makes sure that user is authenticated
    categories = get_config().categories
    return {'categories': categories}
