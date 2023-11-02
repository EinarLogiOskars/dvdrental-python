import json
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask, jsonify
)
from datetime import datetime, timedelta, timezone
from .db import get_db_connection
from flask_jwt_extended import jwt_required

bp = Blueprint('films', __name__, url_prefix='/films')
CORS(bp)

@bp.route('film_list', methods=['GET'])
@jwt_required()
def film_list():
    con = get_db_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM film_list")
    data = cur.fetchall()
    cur.close()
    con.close()
    return data, 200

@bp.route('film/<filmid>', methods=['GET'])
@jwt_required()
def film(filmid):
    if request.method == 'GET':
        con = get_db_connection()
        cur = con.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM film WHERE film_id = '{0}'".format(filmid))
        data = cur.fetchone()
        cur.close()
        con.close()
        return data
    return 'error'