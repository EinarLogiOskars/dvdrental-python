import os
import psycopg2
from flask_cors import CORS
from flask import Flask, render_template
from psycopg2.extras import RealDictCursor


app = Flask(__name__)
CORS(app)

@app.route("/hello")
def hello():
    return "Hello World! Old"

def get_db_connection():
    conn = psycopg2.connect(host='db',
                            database='dvdrental',
                            user='postgres',
                            password='postgres')
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM film;')
    films = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', films=films)

@app.get('/films')
def films():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM film;')
    films = cur.fetchall()
    cur.close()
    conn.close()
    return films

@app.get('/film_list')
def filmList():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM film_list')
    filmList = cur.fetchall()
    cur.close()
    conn.close()
    return filmList