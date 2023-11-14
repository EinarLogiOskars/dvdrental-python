import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
from flask import (
    Blueprint
)
from ..db.db import get_db_connection
from flask_jwt_extended import jwt_required

bp = Blueprint('customers', __name__, url_prefix='/customers')
CORS(bp)

@bp.route('customer_list', methods=['GET'])
@jwt_required()
def customer_list():
    con = get_db_connection()
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM customer_list')
    data = cur.fetchall()
    cur.close()
    con.close()
    return data, 200
