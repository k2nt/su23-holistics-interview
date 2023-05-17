import os

from dotenv import load_dotenv


# Load environment variables
load_dotenv("../.env")


# Absolute path to current file
basedir = os.path.abspath(os.path.dirname(__file__))


IS_RESET_DB = True
if "IS_RESET_DB" in os.environ:
    IS_RESET_DB = bool(os.environ["IS_RESET_DB"])


# Below are definitions for Flask env vars
# Reference for Flask env vars: https://flask.palletsprojects.com/en/1.1.x/config/


SECRET_KEY = "dont_let_anyone_know_about_me"
if "SECRET_KEY" in os.environ:
    SECRET_KEY = os.environ["SECRET_KEY"]

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, '..', 'app.db')}"
if "DATABASE_URI" in os.environ:
    DATABASE_URI = os.environ["DATABASE_URI"]

FLASK_RUN_HOST = "localhost"
if "FLASK_RUN_HOST" in os.environ:
    FLASK_RUN_HOST = os.environ["FLASK_RUN_HOST"]

FLASK_RUN_PORT = "8000"
if "FLASK_RUN_PORT" in os.environ:
    FLASK_RUN_PORT = os.environ["FLASK_RUN_PORT"]
