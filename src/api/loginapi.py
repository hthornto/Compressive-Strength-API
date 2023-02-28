from flask import Blueprint, request, abort, session, Response
from decouple import config
from ..common_elements import Auth

login_api = Blueprint("loginapi", __name__, url_prefix="/api/loginapi")


@login_api.route("/", methods=['POST'])
def login():
    if Auth().login(request=request):
        return Response(status=200)
    else:
        return abort(Auth().getstatus())

    """if "api_key" not in request.json and "api_password" not in request.json:
        return abort(401)

    if request.json['api_key'] == config("API_KEY") and request.json['api_password'] == config("API_PASSWORD"):
        session["loggedin"] = True
        return "Logged in"
    else:
        return abort(401)
    """


@login_api.route("/logout", methods=["GET"])
def logout():
    # session.pop("loggedin", False)
    Auth().logout()

    return abort(401)
