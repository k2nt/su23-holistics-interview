from flask import request
from flask import jsonify
from flask import Blueprint
from flask import make_response

from http import HTTPStatus


fs = Blueprint("fs", __name__)


@fs.route("/cr", methods=["POST"])
def create_file():
    resp = make_response()
    resp.status_code = HTTPStatus.CREATED
    resp.headers['Content-Type'] = 'application/json'
    return resp


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
