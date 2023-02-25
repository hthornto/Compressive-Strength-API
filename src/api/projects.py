from flask import Blueprint, jsonify, abort, request
from ..models import Clients, db, Projects
import sqlalchemy

bp = Blueprint("projects", __name__, url_prefix="/api/projects")


@bp.route("", methods=["GET"])
def index():
    projects = Projects.query.all()
    result = []
    for p in projects:
        result.append(p.serialize())

    return jsonify(result)


@bp.route("/<int:id>", methods=["GET"])
def show(id: int):
    project = Projects.query.get_or_404(id)
    return jsonify(project.serialize())


@bp.route("", methods=["POST"])
def create():
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
    except:
        return jsonify(False)

    # stmt = db.insert(Projects).


@bp.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    # check to see if project id exist
    p = Projects.query.get(id)
    try:
        db.session.delete(p)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route("/<int:id>", methods=["PUT", "PATCH"])
def update(id: int):
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
