import base64
from io import BytesIO
from typing import Union, Annotated
from fastapi import Depends
from pydantic import BaseModel, Field
from PIL import Image

from src.config.config import get_config
from src.db.db import MongoDB
from src.oauth2.oauth2 import get_email
from src.s3.s3 import S3

categories = get_config().categories
validation_config = get_config().validation_config


class UserProfile(BaseModel):
    email: str = Field(..., max_length=validation_config.max_email_length)

    display_name: None | str = Field(None, max_length=validation_config.max_name_length)
    username: None | str = Field(None, max_length=validation_config.max_name_length)
    description: None | str = Field(None, max_length=validation_config.max_description_length)
    teach_categories: None | list[str] = Field(None, enum=categories)
    learn_categories: None | list[str] = Field(None, enum=categories)
    is_public: bool = True
    are_notifications_enabled: bool = True
    is_registered: bool = False

    def update(self, profile: Union['UserProfile', 'UserFillProfile']):
        print(f'Updating user {self.email}')
        if isinstance(profile, UserProfile):
            super().__init__(**profile.model_dump())
        elif isinstance(profile, UserFillProfile):
            super().__init__(
                email=self.email,
                **profile.model_dump(),
                is_public=True,
                are_notifications_enabled=True,
                is_registered=True
            )

    async def apply(self):
        print(f'Applying user {self.email}')
        cursor = MongoDB()

        await cursor.collection.update_one(
            {'email': self.email},
            {'$set': self.model_dump()},
        )

    async def delete(self):
        print(f'Deleting user {self.email}')
        cursor = MongoDB()
        await cursor.collection.delete_one({'email': self.email})


async def get_profile(email: Annotated[str, Depends(get_email)]) -> UserProfile | None:
    cursor = MongoDB()

    user = await cursor.collection.find_one({'email': email})
    if not user:
        return None

    return UserProfile(**user)


class UserGetProfile(BaseModel):
    email: str = Field(..., max_length=validation_config.max_email_length)
    display_name: str = Field(..., max_length=validation_config.max_name_length)
    username: str = Field(..., max_length=validation_config.max_name_length)
    description: str = Field(..., max_length=validation_config.max_description_length)
    teach_categories: list[str] = Field(..., enum=categories)
    learn_categories: list[str] = Field(..., enum=categories)


class UserFillProfile(BaseModel):
    username: str = Field(..., min_length=1, max_length=validation_config.max_name_length)
    display_name: str = Field(..., min_length=1, max_length=validation_config.max_name_length)
    description: str = Field(..., min_length=1, max_length=validation_config.max_description_length)
    teach_categories: list[str] = Field(..., enum=categories)
    learn_categories: list[str] = Field(..., enum=categories)
