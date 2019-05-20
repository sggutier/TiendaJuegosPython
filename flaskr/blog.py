from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.db import get_db_maestro, get_db_esclavo, commit_db
from base64 import b64encode as b64enc
import datetime

bp = Blueprint('blog', __name__)


def encodaPics(pic):
    return b64enc(pic).decode("utf-8")


@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db_esclavo()
    srx = request.form['search'] if request.method == 'POST' else ''
    if srx != '':
        db.execute(
            'SELECT idjuego, nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, stock, descripcion, imagen from productos'
            "  where desarrollador like '%" + srx + "%' ORDER BY fechalanzamiento DESC",
        )
    else:
        db.execute(
            'SELECT idjuego, nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, stock, descripcion, imagen from productos'
            ' ORDER BY fechalanzamiento DESC'
        )
    posts = db.fetchall()
    return render_template('blog/index.html', juegos=posts, encr=encodaPics)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        genero = request.form['genero']
        fechalanzamiento = request.form['fechalanzamiento']
        desarrollador = request.form['desarrollador']
        clasificacion = request.form['clasificacion']
        precio = request.form['precio']
        stock = request.form['stock']
        descripcion = request.form['descripcion']
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
        if not stock:
            errors.append('Se necesita el stock.')
        if not descripcion:
            errors.append('Se necesita el descripcion.')
        if not imagen:
            imagen = None

        if len(errors) > 0:
            flash('\n'.join(errors))
        else:
            try:
                db = get_db_maestro()
                db.execute(
                    'INSERT INTO productos (nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, stock, descripcion, imagen)'
                    ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, stock, descripcion, imagen, )
                )
                commit_db()
            except:
                print('oh, un errorcillo *shrug*')
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html', hoy=datetime.date.today().isoformat())


def get_juego(id, check_author=True):
    db = get_db_esclavo()
    db.execute(
        'SELECT idjuego, nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, stock, descripcion, imagen from productos'
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
        stock = request.form['stock']
        descripcion = request.form['descripcion']
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
        if not stock:
            errors.append('Se necesita el stock.')
        if not descripcion:
            errors.append('Se necesita el descripcion.')

        if len(errors) > 0:
            flash('\n'.join(errors))
        else:
            try:
                db = get_db_maestro()
                if imagen:
                    db.execute(
                        'UPDATE productos SET nombre = %s, genero = %s, fechalanzamiento = %s, desarrollador = %s, clasificacion = %s, precio = %s, stock = %s, descripcion = %s, imagen = %s'
                        ' WHERE idjuego = %s',
                        (nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, stock, descripcion, imagen, id)
                    )
                else:
                    db.execute(
                        'UPDATE productos SET nombre = %s, genero = %s, fechalanzamiento = %s, desarrollador = %s, clasificacion = %s, precio = %s, stock = %s, descripcion = %s'
                        ' WHERE idjuego = %s',
                        (nombre, genero, fechalanzamiento, desarrollador, clasificacion, precio, stock, descripcion, id)
                    )
                commit_db()
            except:
                print('otro error mas :(')
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', juego=juego, encr=encodaPics)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_juego(id)
    db = get_db_maestro()
    db.execute('DELETE FROM productos WHERE idjuego = %s', (id,))
    commit_db()
    return redirect(url_for('blog.index'))


@bp.route('/auditoria', methods=('GET', 'POST'))
def auditoria():
    db = get_db_esclavo(False)
    db.execute(
        'select idaudi, accion, usr, timestamp, idjuegoViejo, nombreViejo, generoViejo, fechalanzamientoViejo, desarrolladorViejo, clasificacionViejo, precioViejo, stockViejo, descripcionViejo, imagenViejo, idjuegoNuevo, nombreNuevo, generoNuevo, fechalanzamientoNuevo, desarrolladorNuevo, clasificacionNuevo, precioNuevo, stockNuevo, descripcionNuevo, imagenNuevo from auditoria'
        ' order by timestamp'
        )
    tabla = db.fetchall()
    return render_template('blog/auditoria.html', lineas=tabla, encr=encodaPics)
