import os

from flask import Flask

import app.lib.service_logging as sv_logging


def configure():
    """Configure infrastructures
    """
    # Set up logging module
    sv_logging.configure("app", is_debug=False)


def create_app(config=None):
    """Create and configure Flask application
    """
    configure()

    sv_logging.info("Starting application ...")
    app = Flask("app")

    sv_logging.info("Configuring application ...")

    # Default application settings
    app.config.from_mapping(
        SECRET_KEY="my_secret_key",
        DATABASE=os.path.join(app.instance_path, "app.sqlite")
        )

    # Load config from config.py if exists
    app.config.from_pyfile("config.py", silent=False)

    sv_logging.info("Establishing database connection ...")

    # Initialize database
    from app.extensions import db
    db.init_app(app)

    sv_logging.info("Preparing database ...")

    # Create tables if not exist
    from app.models.fs import init as init_models_fs
    init_models_fs(app)

    sv_logging.info("Registering services ... ")

    # Register blueprints
    from app.fs import fs
    app.register_blueprint(fs)

    @app.route("/")
    def test_alive():
        return "<p>is_alive</p>"

    import app.config as config
    sv_logging.info(f"Listening at {config.FLASK_RUN_HOST}:{config.FLASK_RUN_PORT}")

    return app
