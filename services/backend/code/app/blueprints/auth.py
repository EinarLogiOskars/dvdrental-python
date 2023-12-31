import functools
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
from flask import (
    Blueprint, request, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
                                unset_jwt_cookies, jwt_required, JWTManager
from datetime import datetime, timedelta, timezone
from ..db.db import get_db_connection

bp = Blueprint('auth', __name__, url_prefix='/auth')
CORS(bp)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username'].lower()
        password = request.form['password']
        connect = get_db_connection()
        cur = connect.cursor(cursor_factory=RealDictCursor)
        error = None

        if not first_name:
            error = 'First name is required.'
        elif not last_name:
            error = 'Last name is required.'
        elif not email:
            error = 'Email is required.'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            
            try:
                cur.execute(
                    "INSERT INTO staff (first_name, last_name, email, username, password, address_id, store_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (first_name, last_name, email, username, generate_password_hash(password), 1, 1),
                )
                connect.commit()
            except connect.IntegrityError:
                error = f"User {username} is already registered."
                cur.close()
                connect.close()
                return error
            else:
                cur.close()
                connect.close()
                return 'Success', 201
            

@bp.route('/disable', methods=['POST'])
@jwt_required()
def disable():
    if request.method == 'POST':
        username = request.form['username']
        error = None
        connection = get_db_connection()
        cur = connection.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute('UPDATE staff SET active = false WHERE username = %s', (username,))
            connection.commit()
        except connection.Error:
            cur.close()
            connection.close()
            error = "Something went wrong!"
            return error
        else:
            cur.close()
            connection.close()
            return "Success", 200
        
@bp.route('/remove', methods=['POST'])
@jwt_required()
def remove():
    if request.method == 'POST':
        username = request.form['username']
        error = None
        con = get_db_connection()
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute('DELETE FROM staff WHERE username = %s', (username,))
            con.commit()
        except:
            error = "Something went wrong. Please make sure you are posting a username that is registered as a string format."
            cur.close()
            con.close()
            return error, 400
        else:
            affectedRow = ('Affected rows: {0}'.format(cur.rowcount))
            cur.close()
            con.close()
            return affectedRow, 200
    

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        error = None
        connection = get_db_connection()
        cur = connection.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            'SELECT * FROM staff WHERE username = %s', (username,)
        )
        user = cur.fetchone()
        cur.close()
        connection.close()

        if user is None or not check_password_hash(user['password'], password):
            return jsonify({"msg": "Incorrect username or password"}), 401
        
        if user['active'] is False:
            return jsonify({"msg": "User is not active"}), 401
        
        access_token = create_access_token(identity=username)
        response = {"access_token":access_token}
        return response


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@bp.after_request
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