from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.db import get_db, commit_db
from base64 import b64encode as b64enc

bp = Blueprint('blog', __name__)


def encodaPics(pic):
    return b64enc(pic).decode("utf-8")


@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    srx = request.form['search'] if request.method == 'POST' else ''
    if srx != '':
        db.execute(
            'SELECT idjuego, nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, rating, publicador, imagen from juegos'
            '  where desarrollador = %s ORDER BY fechalanzamiento DESC',
            (srx,)
        )
    else:
        db.execute(
            'SELECT idjuego, nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, rating, publicador, imagen from juegos'
            ' ORDER BY fechalanzamiento DESC'
        )
    posts = db.fetchall()
    return render_template('blog/index.html', juegos=posts)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        genero = request.form['genero']
        fechalanzamiento = request.form['fechalanzamiento']
        desarrollador = request.form['desarrollador']
        clasificacion = request.form['clasificacion']
        precio = request.form['precio']
        rating = request.form['rating']
        publicador = request.form['publicador']
        imagen = None
        errors = []

        if 'imagen' in request.files:
            imagen = request.files['imagen'].stream.read()

        if not nombre:
            errors.append('Se necesita el nombre.')
        if not genero:
            errors.append('Se necesita el genero.')
        if not fechalanzamiento:
            errors.append('Se necesita la fecha de lanzamiento.')
        if not desarrollador:
            errors.append('Se necesita el desarrollador.')
        if not clasificacion:
            errors.append('Se necesita la clasificacion.')
        if not precio:
            errors.append('Se necesita el precio.')
        if not rating:
            errors.append('Se necesita el rating.')
        if not publicador:
            errors.append('Se necesita el publicador.')
        if not imagen:
            imagen = None

        if len(errors) > 0:
            flash('\n'.join(errors))
        else:
            db = get_db()
            db.execute(
                'INSERT INTO juegos (nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, rating, publicador, imagen)'
                ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, rating, publicador, imagen, )
            )
            commit_db()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_juego(id, check_author=True):
    db = get_db()
    db.execute(
        'SELECT idjuego, nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, rating, publicador, imagen from juegos'
        ' WHERE idjuego = %s',
        (id,)
    )
    post = db.fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    juego = get_juego(id)

    if request.method == 'POST':
        nombre = request.form['nombre']
        genero = request.form['genero']
        fechalanzamiento = request.form['fechalanzamiento']
        desarrollador = request.form['desarrollador']
        clasificacion = request.form['clasificacion']
        precio = request.form['precio']
        rating = request.form['rating']
        publicador = request.form['publicador']
        imagen = None
        errors = []

        if 'imagen' in request.files:
            imagen = request.files['imagen'].stream.read()

        if not nombre:
            errors.append('Se necesita el nombre.')
        if not genero:
            errors.append('Se necesita el genero.')
        if not fechalanzamiento:
            errors.append('Se necesita la fecha de lanzamiento.')
        if not desarrollador:
            errors.append('Se necesita el desarrollador.')
        if not clasificacion:
            errors.append('Se necesita la clasificacion.')
        if not precio:
            errors.append('Se necesita el precio.')
        if not rating:
            errors.append('Se necesita el rating.')
        if not publicador:
            errors.append('Se necesita el publicador.')

        if len(errors) > 0:
            flash('\n'.join(errors))
        else:
            db = get_db()
            if imagen:
                db.execute(
                    'UPDATE juegos SET nombre = %s, genero = %s, fechalanzamiento = %s, desarrollador = %s, clasificacion = %s, precio = %s, rating = %s, publicador = %s, imagen = %s'
                    ' WHERE idjuego = %s',
                    (nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, rating, publicador, imagen, id)
                )
            else:
                db.execute(
                    'UPDATE juegos SET nombre = %s, genero = %s, fechalanzamiento = %s, desarrollador = %s, clasificacion = %s, precio = %s, rating = %s, publicador = %s'
                    ' WHERE idjuego = %s',
                    (nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, rating, publicador, id)
                )
            commit_db()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', juego=juego, encr=encodaPics)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_juego(id)
    db = get_db()
    db.execute('DELETE FROM juegos WHERE idjuego = %s', (id,))
    commit_db()
    return redirect(url_for('blog.index'))
