from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.db import get_db, commit_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
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
        imagen = request.form['imagen']
        errors = []

        if not nombre:
            errors.append('Se necesita el nombre.')
        if not genero:
            errors.append('Se necesita el genero.')
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
            print([nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, rating, publicador, imagen])
            commit_db()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
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
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = %s, body = %s'
                ' WHERE id = %s',
                (title, body, id)
            )
            commit_db()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = %s', (id,))
    commit_db()
    return redirect(url_for('blog.index'))
