from flask import request
from flask import jsonify
from flask import make_response
from flask import Blueprint


fs = Blueprint("fs", __name__)


@fs.route("/cr", methods=["POST"])
def create_file():
    return "<p>cr</p>"


@fs.route("/cat", methods=["GET"])
def get_file_content():
    return f"<p>cat</p>"


@fs.route("/ls", methods=["GET"])
def list_subfiles():
    return f"<p>ls</p>"


@fs.route("/mv", methods=["POST"])
def move_file():
    return f"<p>mv</p>"


@fs.route("/rm", methods=["POST"])
def remove_file():
    return f"<p>rm</p>"


@fs.route("/find_name_pfx", methods=["POST"])
def find_file_by_name_prefix():
    return f"<p>find</p>"


@fs.route("/up", methods=["POST"])
def update_file():
    return f"<p>up</p>"
