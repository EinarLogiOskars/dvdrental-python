import os 
import json
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
                                unset_jwt_cookies, jwt_required, JWTManager
from datetime import datetime, timedelta, timezone
from flask_cors import CORS
from . import auth
from . import films, customers


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    #app.config.from_mapping(
    #    SECRET_KEY='dev'
    #)

    app.config["JWT_SECRET_KEY"] = "dev" #Change this before production!
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    jwt = JWTManager(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                data = response.get_json()
                if type(data) is dict:
                    data["access_token"] = access_token
                    response.data = json.dumps(data)
            return response
        except (RuntimeError, KeyError):
            return response
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(films.bp)
    app.register_blueprint(customers.bp)
    
    return app