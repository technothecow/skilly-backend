from pydantic import BaseModel


class SearchRequest(BaseModel):
    username: str
    learn_categories: list[str]
    teach_categories: list[str]
    page: int

class UserSearchData(BaseModel):
    username: str
    display_name: str
    description: str
    learn_categories: list[str]
    teach_categories: list[str]

class SearchData(BaseModel):
    users: list[UserSearchData]
