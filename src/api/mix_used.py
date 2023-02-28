from flask import Blueprint, request, abort, jsonify, Response
from ..models import MixUsed, Sets, db
from ..common_elements import Auth

mix_used_blueprint = Blueprint("mix used", __name__,
                               url_prefix='/api/compressive-strength/mix-used')


@mix_used_blueprint.route("", methods=['POST'])
def create():
    if Auth().is_logged_in():
        if "producer" not in request.json:
            return abort(400)

        if "mix_description" not in request.json:
            mix_description = None
        else:
            mix_description = request.json["mix_description"]
        if "mix_code" not in request.json:
            mix_code = None
        else:
            mix_code = request.json["mix_code"]
        if "strength" not in request.json:
            strength = None
        else:
            strength = request.json["strength"]
        if "isMRWH" not in request.json:
            isMRWH = False
        else:
            isMRWH = request.json["isMRWH"]
        if "isHRWH" not in request.json:
            isHRWH = False
        else:
            isHRWH = request.json["isHRWH"]

        mix_used = MixUsed(
            producer=request.json["producer"],
            mix_description=mix_description,
            mix_code=mix_code,
            strength=strength,
            isMRWH=isMRWH,
            isHRWH=isHRWH
        )
        try:
            db.session.add(mix_used)
            db.session.commit()
            return mix_used.serialize()
        except:
            return abort(400)
    else:
        return abort(401)


@mix_used_blueprint.route("", methods=['GET'])
def index():
    if Auth().is_logged_in():
        mix_used = MixUsed.query.all()
        results = []
        for m in mix_used:
            results.append(m.serialize())
        return jsonify(results)
    else:
        return abort(401)


@mix_used_blueprint.route("/<int:id>", methods=["GET"])
def show(id: int):
    if Auth().is_logged_in():
        mix_used = db.get_or_404(MixUsed, id)
        return mix_used.serialize()
    else:
        return abort(401)


@mix_used_blueprint.route("/<int:id>", methods=['DELETE'])
def delete(id: int):
    if Auth().is_logged_in():

        mix_used = db.get_or_404(MixUsed, id)
        try:
            db.session.delete(mix_used)
            db.session.commit()
            return Response("Resource deleted", 204)
        except:
            return Response("Could not delete resource", 204)
    else:
        return abort(401)


@mix_used_blueprint.route("/<int:id>", methods=['PUT', 'PATCH'])
def update(id: int):
    if Auth().is_logged_in():
        mix_used = db.get_or_404(MixUsed, id)
        if "producer" in request.json:
            mix_used.producer = request.json['producer']
        if "mix_description" in request.json:
            mix_used.mix_description = request.json["mix_description"]
        if "mix_code" in request.json:
            mix_used.mix_code = request.json["mix_code"]
        if "strength" in request.json:
            mix_used.strength = request.json["strength"]
        if "isMRWH" in request.json:
            mix_used.isMRWH = request.json["isMRWH"]
        if "isHRWH" in request.json:
            mix_used.isHRWH = request.json["isHRWH"]
        db.session.add(mix_used)
        db.session.commit()
        return mix_used.serialize()
    else:
        return abort(401)
