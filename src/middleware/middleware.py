from fastapi.middleware.cors import CORSMiddleware


def setup_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://10.8.0.8:3000"],  # TODO: add valid origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all HTTP methods
        allow_headers=["*"],  # Allows all headers
    )
