import os

from flask import Flask
from dotenv import load_dotenv, dotenv_values

import backend_logging as be_logging
from backend_logging import configure as be_logging_configure
from app_builder import AppContext, build_app


def configure():
    # Load environment variables
    load_dotenv()
    # Configure logging module
    be_logging_configure(sv_name="backend", is_debug=False)


def start():
    be_logging.info("backend")

    # Build Flask app
    ctx = AppContext(
        config={
            "SECRET_KEY": os.environ["SECRET_KEY"],
            "SQLALCHEMY_DATABASE_URI": os.environ["SQLALCHEMY_DATABASE_URI"]
            }
        )
    app = build_app(ctx)

    host = os.environ["FLASK_RUN_HOST"]
    port = int(os.environ["FLASK_RUN_PORT"])
    app.run(host="::1", port=port)


if __name__ == "__main__":
    configure()
    start()
