import json
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask, jsonify
)
from datetime import datetime, timedelta, timezone
from ..db.db import get_db_connection
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import BadRequestKeyError

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

@bp.route('add', methods=['POST'])
@jwt_required()
def add_film():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        release_year = request.form['release_year']
        language_id = request.form['language_id']
        rental_duration = request.form['rental_duration']
        rental_rate = request.form['rental_rate']
        length = request.form['length']
        replacement_cost = request.form['replacement_cost']
        rating = request.form['rating']
        category = request.form['category']
        actor = request.form['actor']
        film_id = None

        con = get_db_connection()
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("INSERT INTO film(title, description, release_year, language_id, rental_duration, rental_rate, length, replacement_cost, rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (title, description, release_year, language_id, rental_duration, rental_rate, length, replacement_cost, rating))
            con.commit()
            cur.execute("SELECT * FROM film WHERE title = %s ORDER BY film_id DESC", (title,))
            film_id = json.dumps(cur.fetchone()['film_id'])
            cur.execute("INSERT INTO film_actor(actor_id, film_id) VALUES (%s, %s)", (actor, film_id))
            con.commit()
            cur.execute("INSERT INTO film_category(film_id, category_id) VALUES (%s, %s)", (film_id, category))
            con.commit()
        except con.DataError:
            cur.close()
            con.close()
            return "Invalid film information", 400
        except con.IntegrityError:
            cur.close()
            con.close()
            return "Invalid language", 400
        else:
            #cur.execute('INSERT INTO film_list(fid, title, description, category, price, length, rating, actors) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            #            (film_id, title, description, category, rental_rate, length, rating, actors))
            cur.close()
            con.close()
            return film_id, 201
        

        
        