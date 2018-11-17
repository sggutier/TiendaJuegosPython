import sqlite3
from flask_mysqldb import MySQL
import click
from flask import current_app, g
from flask.cli import with_appcontext

# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row

#     return g.db


def get_db():
    global mysql
    # if 'db' not in g:
    # g.db = mysql.connection.cursor()
    # return g.db
    return mysql.connection.cursor()


def commit_db():
    global mysql
    mysql.connection.commit()


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        txt = f.read().decode('utf8')
        txt = ''.join(txt.split('\n'))
        lins = txt.split(';')[:-1]
        for lin in lins:
            print('ejecutando: ' + lin)
            db.execute(lin)
            # print(lin)
        # db.execute(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    # current_app.teardown_appcontext(close_db)


def init_app(app):
    global mysql
    mysql = MySQL(app)
    # app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
