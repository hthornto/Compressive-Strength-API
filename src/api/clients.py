from flask import Blueprint, jsonify, abort, request
from ..models import Clients, db

bp = Blueprint("clients", __name__, url_prefix="/api/clients")


@bp.route("", methods=["GET"])
def index():
    clients = Clients.query.all()
    result = []
    for c in clients:
        result.append(c.serialize())

    return jsonify(result)


@bp.route("/<int:id>", methods=["GET"])
def show(id: int):
    clients = Clients.query.get_or_404(id)
    return jsonify(clients.serialize())


@bp.route("", methods=["POST"])
def create():
    if 'name' not in request.json:
        return abort(400)
    if 'address' not in request.json:
        address = None
    else:
        address = request.json["address"]
    if 'city' not in request.json:
        city = None
    else:
        city = request.json["city"]
    if 'state' not in request.json:
        state = None
    else:
        state = request.json["state"]
    if 'postalcode' not in request.json:
        postalcode = None
    else:
        postalcode = request.json["postalcode"]
    if "country" not in request.json:
        country = "USA"
    else:
        country = request.json["country"]
    client = Clients(

        name=request.json["name"],
        address=address,
        city=city,
        state=state,
        postalcode=postalcode,
        country=country,
    )

    db.session.add(client)
    db.session.commit()
    return jsonify(client.serialize())


@bp.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    client = Clients.query.get_or_404(id)
    try:
        db.session.delete(client)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route("/<int:id>", methods=["PATCH", "PUT"])
def update(id: int):
    c = Clients.query.get_or_404(id)
    if "name" in request.json:
        c.name = request.json["name"]
    if 'address' in request.json:
        c.address = request.json["address"]
    if 'city' in request.json:
        c.city = request.json["city"]
    if 'state' in request.json:
        c.state = request.json["state"]
    if 'postalcode' in request.json:
        c.postalcode = request.json["postalcode"]
    if "country" in request.json:
        c.country = request.json["country"]

    try:
        db.session.add(c)
        db.session.commit()
        return jsonify(c.serialize())
    except:
        return jsonify(False)
