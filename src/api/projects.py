from flask import Blueprint, jsonify, abort, request
from ..models import Clients, db, Projects
import sqlalchemy
from ..common_elements import Auth
import logging

bp = Blueprint("projects", __name__, url_prefix="/api/projects")


@bp.route("", methods=["GET"])
def index():
    if Auth().is_logged_in():
        projects = Projects.query.all()
        result = []
        for p in projects:
            result.append(p.serialize())

        return jsonify(result)
    else:
        return abort(401)


@bp.route("/<int:id>", methods=["GET"])
def show(id: int):
    if Auth().is_logged_in():
        project = Projects.query.get_or_404(id)
        return jsonify(project.serialize())
    else:
        return Auth().getAccess()


@bp.route("", methods=["POST"])
def create():
    if Auth().is_logged_in():
        if "name" not in request.json or "client_id" not in request.json:
            return abort(400)
        Clients.query.get(request.json["client_id"])

        p = Projects(
            client_id=request.json["client_id"],
            name=request.json["name"]
        )
        try:
            db.session.add(p)
            db.session.commit()
            return jsonify(p.serialize())
        except BaseException as e:
            logging.critical(e)
            return jsonify(False)
    else:
        return abort(401)
    # stmt = db.insert(Projects).


@bp.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    if Auth().is_logged_in():
        # check to see if project id exist
        p = Projects.query.get(id)
        try:
            db.session.delete(p)
            db.session.commit()
            return jsonify(True)
        except:
            return jsonify(False)
    else:
        return abort(401)


@bp.route("/<int:id>", methods=["PUT", "PATCH"])
def update(id: int):
    if Auth().is_logged_in():
        newname = ""
        new_id = ""

        project_id = Projects.query.get(id)
        if "name" in request.json:
            project_id.name = request.json["name"]
        if "client_id" in request.json:
            project_id.client_id = int(request.json['client_id'])

        try:
            db.session.add(project_id)

            db.session.commit()
            return jsonify(project_id.serialize())

        # return jsonify(True)
        except:
            return jsonify(False)
    else:
        return abort(401)
