import db
from sqlalchemy import Column, String, Integer, Boolean, Date

class Tarea(db.Base):
    '''Clase que crea la tabla Tarea en la bd'''
    __tablename__ = "Tarea"
    id = Column(Integer, primary_key=True)
    contenido = Column(String(200), nullable=False)
    hecha = Column(Boolean, default=False)
    categoria = Column(String(200), default='')
    fecha_limite = Column(Date, default=None)

    def __init__(self, contenido, hecha=False, categoria='', fecha_limite=None):
        self.contenido = contenido
        self.hecha = hecha
        self.categoria = categoria
        self.fecha_limite = fecha_limite

    def __repr__(self):
        return "Tarea {}: {} ({}) {}, {}".format(self.id, self.contenido, self.hecha, self.categoria, self.fecha_limite)

    def __str__(self):
        return "Tarea {}: {} ({}) {}, {}".format(self.id, self.contenido, self.hecha, self.categoria, self.fecha_limite)

class Configuracion(db.Base):
    '''Clase que crea la tabla Configuracion en la bd, sirve para guardar el estado de constantes como del modo oscuro'''
    __tablename__ = 'Configuracion'
    id = Column(Integer, primary_key=True)
    modo_oscuro = Column(Boolean, default=0)
