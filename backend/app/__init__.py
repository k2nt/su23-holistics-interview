import os

from flask import Flask


def create_app(config=None):
    """Create and configure Flask application
    """
    app = Flask("app")

    # Default application settings
    app.config.from_mapping(
        SECRET_KEY="my_secret_key",
        DATABASE=os.path.join(app.instance_path, "app.sqlite")
        )

    # Load config from config.py if exists
    app.config.from_pyfile("config.py", silent=False)

    # Initialize database
    from app.extensions import db
    db.init_app(app)

    # Register blueprints
    from app.fs import fs
    app.register_blueprint(fs)

    @app.route("/")
    def test_alive():
        return "<p>is_alive</p>"

    return app
