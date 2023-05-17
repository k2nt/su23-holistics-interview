from http import HTTPStatus

from flask import request
from flask import Blueprint
from flask import jsonify
from flask import make_response

from app.fs import usecase as uc
from app.lib import service_logging as sv_logging


fs = Blueprint("fs", __name__)


@fs.route("/cr", methods=["POST"])
def create_file():
    req_data = request.get_json()['data']
    print(req_data)
    try:
        uc.create_file(
            path=req_data["path"],
            force_create=req_data["forceCreate"],
            data=req_data["data"]
            )
        resp = make_response()
        resp.status_code = HTTPStatus.CREATED
        return resp
    except Exception as e:
        print(e)
        resp = make_response(jsonify({"msg": str(e)}), HTTPStatus.BAD_REQUEST)
        return resp


@fs.route("/cat", methods=["GET"])
def get_file_content():
    path = request.args.get("path")
    print(path)
    try:
        content = uc.get_file_content(path)
        resp = make_response(jsonify({"data": content}), HTTPStatus.OK)
        resp.headers['Content-Type'] = "application/json"
        return resp
    except Exception as e:
        print(e)
        resp = make_response(jsonify({"msg": str(e)}), HTTPStatus.BAD_REQUEST)
        return resp


@fs.route("/ls", methods=["GET"])
def list_subfiles():
    path = request.args.get("path")
    try:
        li = uc.list_subfiles(path)
        resp = make_response(jsonify({"data": li}), HTTPStatus.OK)
        resp.headers['Content-Type'] = "application/json"
        return resp
    except Exception as e:
        print(e)
        resp = make_response(jsonify({"msg": str(e)}), HTTPStatus.BAD_REQUEST)
        return resp


@fs.route("/mv", methods=["POST"])
def move_file():
    return f"<p>mv</p>"


@fs.route("/rm", methods=["DELETE"])
def remove_file():
    return f"<p>rm</p>"


@fs.route("/find_name_pfx", methods=["POST"])
def find_file_by_name_prefix():
    return f"<p>find</p>"


@fs.route("/up", methods=["UPDATE"])
def update_file():
    return f"<p>up</p>"
