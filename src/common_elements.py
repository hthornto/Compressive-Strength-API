from flask import session, sessions, abort, Response
#from decouple import config
import configparser

class Auth:

    status = 401
    config = configparser.ConfigParser()
    config.read("../settings.ini")
    def login(self, request):
        if "api_key" not in request.json and "api_password" not in request.json:
            self.status = 401
            return False
        if request.json['api_key'] == self.config["General"]["API_KEY"] and request.json['api_password'] == self.config["General"]["API_PASSWORD"]:
            session["loggedin"] = True
            self.status = 200
            return True
        else:
            self.status = 401
            return False

    def logout(self):
        session['loggedin'] = False
        self.status = 401

    def is_logged_in(self):
        if 'loggedin' in session:
            if session['loggedin'] == True:
                self.status = 200
                return True
            else:
                self.status = 401
                return False

    def getstatus(self):
        return self.status

    def getAccess(self):
        return abort(401)
