import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
from flask import (
    Blueprint, request
)
from flask_jwt_extended import jwt_required
from ..db.db import get_db_connection

bp = Blueprint('category', __name__, url_prefix='/category')
CORS(bp)

@bp.route('list', methods=['GET'])
@jwt_required()
def category_list():
    if request.method == 'GET':
        con = get_db_connection()
        cur = con.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM category')
        data = cur.fetchall()
        cur.close()
        con.close()
        return data, 200