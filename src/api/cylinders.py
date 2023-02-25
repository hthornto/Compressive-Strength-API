from flask import Blueprint, views, request, jsonify, abort, Response, json
from ..models import db, Cylinders, Sets, MixDesign
import sqlalchemy


cylinder_blueprint = Blueprint(
    "cylinder", __name__, url_prefix="/api/compressive-strength/cylinder")


@cylinder_blueprint.route("/<int:id>", methods=['DELETE'])
def delete(id: int):
    cylinders = Cylinders.query.get_or_404(id)
    try:
        db.session.delete(cylinders)
        db.session.commit()
        return Response("Resource has been deleted", 204)
    except:
        return Response("Error occured", 204)


@cylinder_blueprint.route("", methods=['POST'])
def create():
    if "recieved" not in request.json:
        recieved = None
    else:
        recieved = request.json["recieved"]
    if "cylinder_type_id" not in request.json and "set_id" not in request.json:
        return abort(400)
    cylinders = Cylinders(
        set_id=request.json['set_id'],
        cylinder_type_id=request.json['cylinder_type_id'],
        recieved=recieved

    )

    try:
        db.session.add(cylinders)
        db.session.commit()
        return cylinders.serialize()
    except:
        return "An error has occurred"


@cylinder_blueprint.route("/<int:id>", methods=['PUT', 'PATCH'])
def update(id: int):
    pass
