from flask import Flask, render_template, request, redirect, url_for, jsonify
import db
from models import Tarea, Configuracion
from datetime import datetime

app = Flask(__name__)

@app.before_request
def agregar_entrada_modo_oscuro():
    '''Esta funcion verifica que haya una entrada referente al modo oscuro en la bd, en caso que no haya la crea'''
    configuracion = db.session.query(Configuracion).first()
    if not configuracion:
        nuevo_estado = 0
        modo = Configuracion(modo_oscuro=nuevo_estado)
        db.session.add(modo)
        db.session.commit()

@app.route('/')
def home():
    '''Funcion home que chequea el estado en la base de datos del modo oscuro y devuelve un template u otro en consecuencia'''
    configuracion = db.session.query(Configuracion).first()
    modo_oscuro = bool(configuracion.modo_oscuro)
    if modo_oscuro == 0:
        todas_las_tareas = db.session.query(Tarea).all()
        return render_template("index.html", lista_de_tareas = todas_las_tareas)
    else:
        todas_las_tareas = db.session.query(Tarea).all()
        return render_template('index.html', lista_de_tareas = todas_las_tareas, modo_oscuro=True)

@app.route('/crear-tarea', methods=['POST'])
def crear():
    '''Funcion que crea la tarea, pide el ingreso de texto del usuario y guarda la tarea en la bd'''
    contenido = request.form['la_tarea']
    hecha=False
    categoria=request.form.get('categoria','')
    fecha_limite_str = request.form.get('fecha_limite','')
    if fecha_limite_str:
        fecha_limite=datetime.strptime(fecha_limite_str, '%Y-%m-%d').date()
    else:
        fecha_limite=None
    tarea = Tarea(contenido, hecha, categoria, fecha_limite)
    db.session.add(tarea)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/eliminar-tarea/<id>')
def eliminar(id):
    '''Funcion que lee el id de la tarea especifica y la eliminade bd'''
    eliminar = db.session.query(Tarea).filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/tarea-hecha/<id>')
def hecha(id):
    '''Permite modificar el estado de Hecho de la tarea a 0 o 1'''
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
    tarea.hecha = not(tarea.hecha)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/editar-tarea/<id>', methods=['POST'])
def editar_tarea(id):
    '''Funcion permite editar la tarea, puede cambiar la tarea, categoria y fecha, si no se modificanada queda como estaba'''
    tarea = db.session.query(Tarea).get(id)
    if tarea:
        nueva_tarea = request.form['nuevo_contenido']
        if nueva_tarea:
            tarea.contenido = nueva_tarea
        else:
            tarea.contenido = tarea.contenido
        tarea.categoria = request.form['nueva_categoria']
        fecha_limite_str = request.form.get('nueva_fecha_limite', '')
        if fecha_limite_str:
            tarea.fecha_limite = datetime.strptime(fecha_limite_str, '%Y-%m-%d').date()
        else:
            tarea.fecha_limite = None
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/cambiar-modo-oscuro', methods=['POST'])
def cambiar_modo_oscuro():
    '''Funcion que consulta el modo oscuro y lo cambia, permite activar o desactivar el modo oscuro'''
    configuracion = db.session.query(Configuracion).first()
    modo_oscuro = bool(configuracion.modo_oscuro)
    if modo_oscuro == 0:
        nuevo_estado = 1 # Cambiar a 1 para activar el modo oscuro
    else:
        nuevo_estado = 0
    configuracion.modo_oscuro = nuevo_estado
    db.session.commit()
    return jsonify({'modo_oscuro': nuevo_estado})

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)