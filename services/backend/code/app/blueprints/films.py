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

@bp.route('film_list/<filmid>', methods=['GET'])
@jwt_required()
def film_list_entry(filmid):
    if request.method == 'GET':
        con = get_db_connection()
        cur = con.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM film_list WHERE fid = '{}'".format(filmid))
        data = cur.fetchone()
        cur.close()
        con.close()
        return data, 200
    return 'error'

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
        return data, 200
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
        category = request.form['category'].split(',')
        actor = request.form['actor'].split(',')
        film_id = None

        con = get_db_connection()
        cur = con.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("INSERT INTO film(title, description, release_year, language_id, rental_duration, rental_rate, length, replacement_cost, rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (title, description, release_year, language_id, rental_duration, rental_rate, length, replacement_cost, rating))
            con.commit()
            cur.execute("SELECT * FROM film WHERE title = %s ORDER BY film_id DESC", (title,))
            film_id = json.dumps(cur.fetchone()['film_id'])
            for a in actor:
                cur.execute("INSERT INTO film_actor(film_id, actor_id) VALUES ({0}, {1})".format(film_id, a))
                con.commit()
            for c in category:
                cur.execute("INSERT INTO film_category(film_id, category_id) VALUES ({0}, {1})".format(film_id, c))
                con.commit()
        except con.DataError:
            cur.close()
            con.close()
            return "Invalid film information", 400
        except con.IntegrityError:
            cur.close()
            con.close()
            return "Invalid language or category", 400
        else:
            cur.close()
            con.close()
            return film_id, 201
        
@bp.route('remove', methods=['POST'])
@jwt_required()
def remove_film():
    if request.method == 'POST':
        film_id = request.form['film_id']
        error = None
        con = get_db_connection()
        cur = con.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute('DELETE FROM film WHERE film_id = {0}'.format(film_id))
            con.commit()
        except:
            error = "Something went wrong. Please make sure you are posting a film_id that is registered."
            cur.close()
            con.close()
            return error, 400
        else:
            affectedRow = ('Affected rows: {0}'.format(cur.rowcount))
            cur.close()
            con.close()
            return affectedRow, 200

        

        
        