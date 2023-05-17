from flask import Flask

from .routes import fs
from .repo import create_file, get_file_id


__all__ = ["fs", "init"]


def init(app: Flask):
    with app.app_context():
        # Create root folder
        try:
            get_file_id(path="", is_folder=True)
        except FileNotFoundError:
            create_file(path="", pid=-1, is_folder=True)
