from flask import blueprints, request, jsonify, abort
from ..models import MixDesign, db
from ..common_elements import Auth

bp = blueprints.Blueprint("mix design", __name__,
                          url_prefix="/api/mix-design")


@bp.route("", methods=['POST'])
def create():
    if Auth().is_logged_in():
        if "project_id" not in request.json:
            return abort(400)
        if "producer" not in request.json:
            my_producer = None
        else:
            my_producer = request.json["producer"]
        if "max slump" not in request.json:
            my_max_slump = None
        else:
            my_max_slump = request.json["max slump"]
        if "min slump" not in request.json:
            my_min_slump = None
        else:
            my_min_slump = request.json["min slump"]
        if "max air content" not in request.json:
            my_max_air_content = None
        else:
            my_max_air_content = request.json["max air content"]
        if "min air content" not in request.json:
            my_min_air_content = None
        else:
            my_min_air_content = request.json["min air content"]
        if "MRWH max slump" not in request.json:
            my_mid_range_max_slump = None
        else:
            my_mid_range_max_slump = request.json["MRWH max slump"]
        if "MRWH min slump" not in request.json:
            my_mid_range_min_slump = None
        else:
            my_mid_range_min_slump = request.json["MRWH min slump"]
        if "HRWH max slump" not in request.json:
            my_high_range_max_slump = None
        else:
            my_high_range_max_slump = request.json["HRWH max slump"]
        if "HRWH min slump" not in request.json:
            my_high_range_min_slump = None
        else:
            my_high_range_min_slump = request.json["HRWH min slump"]
        if "break_schedule" in request.json:
            break_schedule = request.json['break_schedule']
        else:
            return abort(400)

        mix_design = MixDesign(
            producer=my_producer,
            max_slump=my_max_slump,
            min_slump=my_min_slump,
            max_air_content=my_max_air_content,
            min_air_content=my_min_air_content,
            mid_range_max_slump=my_mid_range_max_slump,
            mid_range_min_slump=my_mid_range_min_slump,
            high_range_max_slump=my_high_range_max_slump,
            high_range_min_slump=my_high_range_min_slump,
            design_strength=request.json["design_strength"],
            project_id=request.json["project_id"],
            break_schedule=break_schedule,
            # set_id=request.json["set_id"]
        )
        db.session.add(mix_design)
        db.session.commit()
        return jsonify(mix_design.serialize())
    else:
        return abort(401)


@bp.route("", methods=['GET'])
def index():
    if Auth().is_logged_in():
        mix_design = MixDesign.query.all()
        result = []
        for m in mix_design:
            result.append(m.serialize())
        return jsonify(result)
    else:
        return abort(401)


@bp.route("/<int:id>", methods=['GET'])
def show(id: int):
    if Auth().is_logged_in():
        mix_design = MixDesign.query.get_or_404(id)
        return jsonify(mix_design.serialize())
    else:
        return abort(401)


@bp.route("/<int:id>", methods=['DELETE'])
def delete(id: int):
    if Auth().is_logged_in():
        mix_design = MixDesign.query.get(id)
        if mix_design is None:
            return "ERROR HAS OCCURED"
        else:

            return "Resource does not exist"
    else:
        return abort(401)


@bp.route("/<int:id>", methods=['PATCH', 'PUT'])
def update(id: int):
    if Auth().is_logged_in():
        mix_design = MixDesign.query.get(id)
        if "producer" in request.json:
            mix_design.producer = request.json["producer"]
        if "max slump" in request.json:
            mix_design.max_slump = request.json["max slump"]
        if "min slump" in request.json:
            mix_design.min_slump = request.json["min slump"]
        if "max air content" in request.json:
            mix_design.max_air_content = request.json["max air content"]
        if "min air content" in request.json:
            mix_design.min_air_content = request.json["min air content"]
        if "MRWH max slump" in request.json:
            mix_design.mid_range_max_slump = request.json["MRWH max slump"]
        if "MRWH min slump" in request.json:
            mix_design.mid_range_min_slump = request.json["MRWH min slump"]
        if "HRWH max slump" in request.json:
            mix_design.high_range_max_slump = request.json["HRWH max slump"]
        if "HRWH min slump" in request.json:
            mix_design.high_range_min_slump = request.json["HRWH min slump"]
        db.session.add(mix_design)
        db.session.commit()
        return jsonify(mix_design.serialize())
    else:
        return abort(401)
