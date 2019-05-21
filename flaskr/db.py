import mysql.connector as elconector
from flask_mysqldb import MySQL
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db_maestro(dico=True):
    global maestro
    maestro = elconector.connect(
        host="localhost",
        user="anita",
        database="ventas",
        passwd="lagordalagartonanotragaladrogalatina"
    )
    return maestro.cursor(dictionary=dico)


def get_db_esclavo(dico=True):
    global maestro, esclavo
    # esclavo = elconector.connect(
    #     host="192.168.43.4",
    #     user="remotron",
    #     database="ventas",
    #     passwd="password"
    # )
    esclavo = maestro
    return esclavo.cursor(dictionary=dico)


def commit_db():
    global maestro
    maestro.commit()


def init_db():
    db = get_db_maestro()

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
    global maestro, esclavo
    maestro = elconector.connect(
        host="localhost",
        user="anita",
        database="ventas",
        passwd="lagordalagartonanotragaladrogalatina"
    )
    # esclavo = elconector.connect(
    #     host="192.168.31.207",
    #     user="remotron",
    #     database="ventas",
    #     passwd="password"
    # )
    # esclavo = maestro
    # mysql = MySQL(app)
    # app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
