from flask import Blueprint, views, request, jsonify, abort, Response, json, session
from ..models import db, Cylinders, Sets, MixDesign, Specimen_Type
import sqlalchemy
from sqlalchemy.orm import aliased
import math

set_blueprint = Blueprint(
    "sets", __name__, url_prefix="/api/compressive-strength")
# set_blueprint.add_url_rule


class SetJoins:

    def beginner_join(self, model1, model2, name1, name2):
        stmt = (sqlalchemy.select(model1, model2).join_from(
            model1, model2).subquery())
        first_alias = aliased(model1, stmt, name=name1)
        second_alias = sqlalchemy.orm.aliased(
            model2, stmt, name=name2)
        return (first_alias, second_alias)

    def common_join(self, model1, model2, name1, name2):
        stmt = self.beginner_join(model1, model2, name1, name2)
        # first_alias = aliased(model1, stmt, name=name1)
        # second_alias = sqlalchemy.orm.aliased(
        #    model2, stmt, name=name2)

        first_alias = stmt[0]

        second_alias = stmt[1]
        newstmt = sqlalchemy.select(first_alias, second_alias)
        return db.session.execute(newstmt)

    def where_common_join(self, first_alias, second_alias, id, alias):
        newstmt = sqlalchemy.select(
            first_alias, second_alias).where(alias == id)
        return db.session.execute(newstmt)

    def cylinder_set_serialize(self, myresult, multiple=True):
        results = []
        cylinder_result = []
        sets_result = []

        for row in myresult:
            sets = {
                'id': f"{row.sets.id}",
                'slump': f"{row.sets.slump}",
                'air_content': f"{row.sets.air_content}",
                'temperature': f"{row.sets.temperature}",
                'ticket_number': f"{row.sets.ticket_number}",
                'mix_id': f"{row.sets.mix_id}",
                'total_cy': f"{row.sets.total_cy}",
                'project_id': f"{row.sets.project_id}",
                'field_tech_id': f"{row.sets.field_tech_id}",
                'mix_used_id': f"{row.sets.mix_used_id}",

            }
            cylinders = {
                "id": f"{row.cylinders.id}",
                "set_id": f"{row.cylinders.set_id}",
                "max_load": f"{row.cylinders.max_load}",
                "dia1": f"{row.cylinders.dia1}",
                "dia2": f"{row.cylinders.dia2}",
                "break_strength": f"{row.cylinders.break_strength}",
                "cylinder_type_id": f"{row.cylinders.cylinder_type_id}",
                "break_type": f"{row.cylinders.break_type}",
                "weight": f"{row.cylinders.weight}",
                "lab_tech_id": f"{row.cylinders.lab_tech_id}",
                "recieved": f"{row.cylinders.recieved}",
                "age": f"{row.cylinders.break_age}",
                "hold": f"{row.cylinders.on_hold}",
            }

            sets_result.append(sets)
            cylinder_result.append(cylinders)
        if multiple == False:
            myset = {
                "Set": sets_result[0]
            }
            myset["Set"]["Cylinders"] = cylinder_result
            results.append(myset)
        else:

            for s in sets_result:
                myset = {
                    "Set": s
                }
                cylinders = []
                for c in cylinder_result:
                    if c["set_id"] == s["id"]:
                        cylinders.append(c)
                myset["Set"]["Cylinders"] = cylinders
                results.append(myset)

        return results

# Create a set of cylinders


@set_blueprint.route("", methods=["POST"])
def create():
    if "project_id" not in request.json or "number of cylinders" not in request.json or "mix_id" not in request.json:
        return abort(400)

    obtain_mix_id = db.get_or_404(MixDesign, request.json['mix_id'])

    if "total_cy" not in request.json:
        new_total_cy = None
    else:
        new_total_cy = request.json['total_cy']
    if "slump" not in request.json:
        new_slump = None
    else:
        new_slump = request.json['slump'],
    if "air_content" in request.json:
        new_air_content = request.json['air_content']
    else:
        new_air_content = None
    if "temperature" not in request.json:
        temperature = None
    else:
        temperature = request.json['temperature']
    if "ticket_number" not in request.json:
        ticket_number = None
    else:
        ticket_number = request.json['ticket_number']
    if "field_tech_id" in request.json:
        field_tech_id = request.json['field_tech_id']
    else:
        field_tech_id = None
    if "mix_used_id" not in request.json:
        my_mix_used_id = None
    else:
        my_mix_used_id = request.json['mix_used_id']

    sets = Sets(
        # id=request.json['id'],
        slump=new_slump,
        air_content=new_air_content,
        temperature=temperature,
        ticket_number=ticket_number,
        total_cy=new_total_cy,
        project_id=obtain_mix_id.project_id,
        field_tech_id=field_tech_id,
        mix_id=request.json['mix_id'],
        mix_used_id=my_mix_used_id
        # mix_used_id=request.json['mix_used_id']


    )
    db.session.add(sets)
    db.session.commit()

    results = []
    endloop = request.json["number of cylinders"]
    x = 0
    cylinder_results = []
    if "recieved" not in request.json:
        recieved = None
    else:
        recieved = request.json['recieved']
    # while x != endloop:
    for mixid in obtain_mix_id.break_schedule:

        cylinders = Cylinders(
            set_id=sets.id,
            cylinder_type_id=request.json['cylinder_type_id'],
            recieved=recieved,
            break_age=mixid['age'],
            on_hold=mixid['hold'],
        )
        results.append(cylinders)
        cylinder_results.append(cylinders.serialize())
        # x += 1

    db.session.add_all(results)
    db.session.commit()

    result = {
        "set": sets.serialize(),
        "cylinders": cylinder_results,
    }

    return jsonify(result)

# Show all sets and associated information


@set_blueprint.route("", methods=["GET"])
def index():
    # sets = sqlalchemy.alias(Sets)

    # sets = Sets.query.all()
    joins = SetJoins()
    myresult = joins.common_join(Sets, Cylinders, "sets", "cylinders")
    results = joins.cylinder_set_serialize(myresult)
    return results


@set_blueprint.route("/<int:id>", methods=['PUT', 'PATCH'])
def update_set(id: int):
    sets = Sets.query.get_or_404(id)
    if "slump" in request.json:
        sets.slump = request.json['slump']
    if "air_content" in request.json:
        sets.air_content = request.json['air_content']
    if "temperature" in request.json:
        sets.temperature = request.json['temperature']
    if "ticket_number" in request.json:
        sets.ticket_number = request.json['ticket_number']
    if "mix_id" in request.json:
        sets.mix_id = request.json['mix_id']
    if "total_cy" in request.json:
        sets.total_cy = request.json['total_cy']
    if "project_id" in request.json:
        sets.project_id = request.json['project_id']
    if "field_tech_id" in request.json:
        sets.field_tech_id = request.json['field_tech_id']
    if "mix_used_id" in request.json:
        sets.mix_used_id = request.json['mix_used_id']
    try:
        db.session.add(sets)
        db.session.commit()
        return sets.serialize()
    except:
        return abort(204)


@set_blueprint.route("/projects/<int:id>", methods=["GET"])
def show_by_project(id: int):
    joins = SetJoins()
    stmt = joins.beginner_join(Sets, Cylinders, "sets", "cylinders")
    first_alias = stmt[0]
    second_alias = stmt[1]
    newstmt = sqlalchemy.select(first_alias, second_alias).where(
        first_alias.project_id == str(id))
    # myresult = joins.where_common_join(
    #    first_alias, second_alias, str(id), first_alias.project_id)
    myresult = db.session.execute(newstmt)
    return joins.cylinder_set_serialize(myresult)

# Show only one set of specimens


@set_blueprint.route("/<int:id>", methods=["GET"])
def show_by_one(id: int):

    joins = SetJoins()
    stmt = joins.beginner_join(Sets, Cylinders, "sets", "cylinders")
    first_alias = stmt[0]
    second_alias = stmt[1]
    newstmt = sqlalchemy.select(first_alias, second_alias).where(
        second_alias.set_id == id)
    # myresult = joins.where_common_join(
    #    first_alias, second_alias, str(id), first_alias.project_id)
    myresult = db.session.execute(newstmt)
    return joins.cylinder_set_serialize(myresult, multiple=False)

# Delete a set of specimens


@set_blueprint.route("/<int:id>", methods=['DELETE'])
def delete_set(id: int):
    sets = Sets.query.get_or_404(id)
    try:
        db.session.delete(sets)
        db.session.commit()
        return Response("Resouce deleted", 204)

    except:
        return Response("Error occured", 204)
        # return "NO"

# update multiple cylinders at a time


@set_blueprint.route("", methods=["PUT", "PATCH"])
def bulk_update_cylinders():
    x = 0
    results = []
    for c in request.json:

        cylinders = Cylinders.query.get(c["id"])
        if 'dia2' in c:
            cylinders.dia2 = c['dia2']
        if 'dia1' in c:
            cylinders.dia1 = c['dia1']
        if "set_id" in c:
            cylinders.set_id = c["set_id"]
        if "max_load" in c:
            cylinders.max_load = c["max_load"]
            # "break_strength": self.break_strength,
        if "cylinder_type_id" in c:
            cylinders.cylinder_type_id = c["cylinder_type_id"]
        if "break_type" in c:
            cylinders.break_type = c["break_type"]
        if "weight" in c:
            cylinders.weight = c["weight"]
        if "lab_tech_id" in c:
            cylinders.lab_tech_id = c["lab_tech_id"]
        if "recieved" in c:
            cylinders.recieved = c["recieved"]
        if "age" in c:
            cylinders.break_age = c['age']
        if 'hold' in c:
            cylinders.on_hold = c['hold']
        # Determine the stregth of the specimen
        if cylinders.max_load is not None and cylinders.cylinder_type_id is not None and cylinders.dia1 is not None and cylinders.dia2 is not None:
            specimen_type = Specimen_Type.query.get_or_404(
                cylinders.cylinder_type_id)
            # Cylinder Area first then strength
            if specimen_type.speciman_type == "cylinder":
                radius = (cylinders.dia1 + cylinders.dia1)/2 / 2
                area = math.pi * math.pow(radius, 2)
                if radius > 0:
                    cylinders.break_strength = float(cylinders.max_load/area)
                    # return cylinders.break_strength
            elif specimen_type.speciman_type == "prism":

                area = cylinders.dia1 * cylinders.dia1
                if area > 0:
                    cylinders.break_strength = float(cylinders.max_load/area)
            elif specimen_type.speciman_type == "cube":

                area = cylinders.dia1 * cylinders.dia1
                if area > 0:
                    cylinders.break_strength = float(cylinders.max_load/area)
            else:
                return "Type not found"
        else:
            return {"id": cylinders.cylinder_type_id,
                    "load": cylinders.max_load,
                    "dia1": cylinders.dia1,
                    "dia2": cylinders.dia2,
                    }
        results.append(cylinders)

    db.session.add_all(results)
    db.session.commit()
    response = []
    for row in results:
        response.append(row.serialize())
    return response
