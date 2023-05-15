import os
from dataclasses import dataclass
from typing import Dict, Any

from flask import Flask, Blueprint, abort
from dotenv import dotenv_values


__all__ = ["AppContext", "build_app"]


@dataclass(init=True)
class AppContext:
    config: Dict[str, Any] = None


def build_app(ctx: AppContext) -> Flask:
    """Build backend Flask application

    Args:
        ctx: AppContext

    Return:
        Flask
    """
    app = Flask(__name__, instance_relative_config=True)

    # Default config
    app.config.from_mapping(
        SECRET_KEY="dont_let_anyone_know_about_me",
        DATABASE=os.path.join(app.instance_path, "fs.db")
        )

    if ctx.config is None:
        # If user did not provide custom config then try to load it from .env file
        app.config.from_mapping(dotenv_values(), silent=True)
    else:
        # Otherwise update app config with custom config
        app.config.update(ctx.config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def hello():
        return "<p>fs</p>"

    # Register database

    return app
