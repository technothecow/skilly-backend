import importlib
import logging
import pathlib

from fastapi import FastAPI

from src.middleware.middleware import setup_middleware
from src.utils.route_loader import load_routes
from src.config.config import get_config

app = FastAPI()

setup_middleware(app)
load_routes(app, "src/views", "")

if __name__ == '__main__':
    import uvicorn
    server_config = get_config().server_config
    uvicorn.run(app, host=server_config.host, port=server_config.port)
