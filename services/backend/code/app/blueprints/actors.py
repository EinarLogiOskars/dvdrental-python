import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
from flask import (
    Blueprint, request
)
from ..db.db import get_db_connection
from flask_jwt_extended import jwt_required

bp = Blueprint('actors', __name__, url_prefix='/actors')
CORS(bp)

@bp.route('/list', methods=['GET'])
@jwt_required()
def actor_list():
    if request.method == 'GET':
        con = get_db_connection()
        cur = con.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM actor')
        data = cur.fetchall()
        cur.close()
        con.close()
        return data, 200