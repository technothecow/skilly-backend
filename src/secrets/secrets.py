import os


def get_secret(key):
    return os.getenv(key)
