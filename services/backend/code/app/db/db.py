import click
import psycopg2
from flask import current_app, g

def get_db_connection():
    if 'db' not in g:
        g.db = psycopg2.connect(host='db',
                            database='dvdrental',
                            user='postgres',
                            password='postgres')
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db_connection()