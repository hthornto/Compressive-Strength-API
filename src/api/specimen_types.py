import flask
from ..models import Specimen_Type, db
from flask import request, abort
from ..common_elements import Auth

speciman_types = flask.Blueprint(
    "types", __name__, url_prefix="/api/compressive-strength/specimen-types/")


@speciman_types.route("", methods=['POST'])
def create():
    if Auth().is_logged_in():
        if 'size' not in request.json and 'specimen_type' not in request.json:
            errormessage = {}
            key_message = "The key {} is not used!"

            if 'size' not in request.json:
                errormessage['error size'] = key_message.format("size")
            if 'specimen_type' not in request.json:
                errormessage['error specimen_type'] = key_message.format(
                    "specimen_type")
            return flask.jsonify(errormessage)
        else:

            specimen_types = Specimen_Type(
                size=request.json["size"],
                speciman_type=request.json["specimen_type"]
            )
            try:
                db.session.add(specimen_types)
                db.session.commit()
                return flask.jsonify(specimen_types.serialize())
            except:
                return "Unable to add speciman types. Please check the your json request."
    else:
        return abort(401)


@speciman_types.route("", methods=["GET"])
def index():
    if Auth().is_logged_in():
        s = Specimen_Type.query.all()
        results = []
        for r in s:
            results.append(r.serialize())
        return flask.jsonify(results)
    else:
        return abort(401)


@speciman_types.route("<int:id>", methods=['GET'])
def show(id: int):
    if Auth().is_logged_in():
        spt = Specimen_Type.query.get(id)
        if spt is None:
            return flask.abort(404)

        return flask.jsonify(spt.serialize())
    else:
        return abort(401)


@speciman_types.route("<int:id>", methods=['DELETE'])
def delete(id: int):
    if Auth().is_logged_in():
        spt = Specimen_Type.query.get(id)
        if spt is None:
            return flask.abort(404)
        try:
            db.session.delete(spt)
            db.session.commit()
            return flask.Response("Resource has been deleted", 204)
        except:
            return flask.abort(403)
    else:
        return abort(401)


@speciman_types.route("<int:id>", methods=['PUT', 'PATCH'])
def update(id: int):
    if Auth().is_logged_in():
        spt = Specimen_Type.query.get_or_404(id)
        """if spt is None:
            return flask.abort(404)
        """
        if "size" in request.json:
            spt.shape = request.json["size"]
        if "specimen_type" in request.json:
            spt.speciman_type = request.json["specimen_type"]
        try:
            db.session.add(spt)
            db.session.commit()
            return flask.jsonify(spt.serialize())
        except:
            return flask.abort(409)
    else:
        return abort(401)
