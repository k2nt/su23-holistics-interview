import os
from flask import Flask

import app.lib.service_logging as sv_logging
from app.models import *


def configure():
    """Configure infrastructures
    """
    # Set up logging module
    sv_logging.configure("app", is_debug=True)


def create_app(config=None):
    """Create and configure Flask application
    """
    configure()

    sv_logging.info("Starting application ...")
    be_app = Flask("app")

    sv_logging.info("Configuring application ...")

    # Load run-time configs
    import app.config as config

    # Default application settings
    be_app.config.from_mapping(
        SECRET_KEY="my_secret_key",
        DATABASE=os.path.join(be_app.instance_path, "app.sqlite")
        )

    # Load config from config.py if exists
    be_app.config.from_pyfile("config.py", silent=False)

    sv_logging.info("Establishing dependencies ...")

    # Enable CORS
    from app.extensions import cors
    cors.init_app(be_app)

    # Initialize database
    from app.extensions import db
    db.init_app(be_app)

    # Create tables if not exist
    sv_logging.info("Preparing database ...")
    with be_app.app_context():
        if config.IS_RESET_DB:
            db.drop_all()
        db.create_all()

    # Register blueprints
    sv_logging.info("Registering services ...")

    from app.fs import fs, init as init_fs
    init_fs(be_app)
    be_app.register_blueprint(fs, url_prefix="/fs")

    @be_app.route("/")
    def test_alive():
        return "<p>is_alive</p>"

    sv_logging.info(f"Listening at {config.FLASK_RUN_HOST}:{config.FLASK_RUN_PORT}")

    return be_app
