from motor.motor_asyncio import AsyncIOMotorClient

from src.config.config import get_config


class MongoDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)

            mongo_config = get_config().mongo_config
            cls._instance.client = AsyncIOMotorClient(
                f'mongodb://{mongo_config.username}:{mongo_config.password}@'
                f'{mongo_config.host}:{mongo_config.port}/')
            cls._instance.db = cls._instance.client[mongo_config.db]
            cls._instance.collection = cls._instance.db[mongo_config.collection_name]
        return cls._instance

    def get_instance(self):
        return self._instance
