from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        text, create_engine)
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, ma


class CabeceraDetalle(db.Model, SerializerMixin):
    __tablename__ = 'cabecera_detalle'

    id = db.Column(Integer, primary_key=True)
    importe_total = db.Column(Float(asdecimal=True),
                              server_default=text("'0'"))
    pedido = db.Column(ForeignKey('pedido.id',
                                  onupdate='CASCADE'), nullable=False, index=True)

    pedido1 = db.relationship('Pedido')

    def ver(self):
        return '<DetailHead {}>'.format(self.id)

    def __init__(self, imp_tot, ped, ped1):
        self.importe_total = imp_tot
        self.pedido = ped
        self.pedido1 = ped1
        print('<CabeceraDetalle {}>:{}'.format(self.id, self.__dict__))


class HistorialStock(db.Model, SerializerMixin):
    __tablename__ = 'historial_stock'

    id = db.Column(Integer, primary_key=True)
    fecha_hora_movimiento = db.Column(DateTime, nullable=False, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    cantidad = db.Column(Float(asdecimal=True), nullable=False,
                         server_default=text("'0'"))
    unidad = db.Column(Integer, nullable=False)
    signo = db.Column(Integer, nullable=False, server_default=text("'0'"))
    linea_detalle = db.Column(Integer)

    def ver(self):
        return '<History {}>'.format(self.id)

    def __init__(self, fecha_h_m, cant, uni, sig, linea_det):
        self.fecha_hora_movimiento = fecha_h_m
        self.cantidad = cant
        self.unidad = uni
        self.signo = sig
        self.linea_detalle = linea_det
        print('<HistorialStock {}>:{}'.format(self.id, self.__dict__))


class Ingrediente(db.Model, SerializerMixin):
    __tablename__ = 'ingrediente'

    id = db.Column(Integer, primary_key=True)
    nombre = db.Column(String(45), nullable=False)
    descripcion = db.Column(String(120))
    cantidad = db.Column(Float(asdecimal=True), nullable=False)
    unidad = db.Column(ForeignKey('unidad.id',
                                  onupdate='CASCADE'), nullable=False, index=True)

    unidad1 = db.relationship('Unidad')

    def ver(self):
        return '<Ingredient {}>'.format(self.nombre)

    def __init__(self, nom, desc, cant, uni):
        self.nombre = nom
        self.descripcion = desc
        self.cantidad = cant
        self.unidad = uni
        print('<Ingrediente {}>:{}'.format(self.nombre, self.__dict__))


class LineaDetalle(db.Model, SerializerMixin):
    __tablename__ = 'linea_detalle'

    id = db.Column(Integer, primary_key=True)
    cabecera = db.Column(ForeignKey('cabecera_detalle.id',
                                    onupdate='CASCADE'), nullable=False, index=True)
    producto = db.Column(ForeignKey('producto.id',
                                    onupdate='CASCADE'), nullable=False, index=True)
    cantidad = db.Column(Float(asdecimal=True))
    subtotal = db.Column(Float(asdecimal=True))

    cabecera_detalle = db.relationship('CabeceraDetalle')
    producto1 = db.relationship('Producto')

    def ver(self):
        return '<DetailLine {}>'.format(self.id)

    def __init__(self, cabe, prod, cant, subt):
        self.cabecera = cabe
        self.producto = prod
        self.cantidad = cant
        self.subtotal = subt
        print('<LineaDetalle {}>:{}'.format(self.id, self.__dict__))


class Pedido(db.Model, SerializerMixin):
    __tablename__ = 'pedido'

    id = db.Column(Integer, primary_key=True)
    nro_pedido = db.Column(Integer, nullable=False)
    estado = db.Column(String(45))
    fecha_hora_entrega = db.Column(DateTime)
    orden_fabricacion = db.Column(Integer)
    solicitante = db.Column(ForeignKey('usuario.id'),
                            nullable=False, index=True)

    usuario = db.relationship('Usuario')

    def ver(self):
        return '<Delivery {}>'.format(self.nro_pedido)

    def __init__(self, nro_ped, est, orden_fab, solic):
        self.nro_pedido = nro_ped
        self.estado = est
        self.orden_fabricacion = orden_fab
        self.solicitante = solic
        print('<Pedido {}>:{}'.format(self.nro_pedido, self.__dict__))


class Producto(db.Model, SerializerMixin):
    __tablename__ = 'producto'

    id = db.Column(Integer, primary_key=True)
    nombre = db.Column(String(45), nullable=False)
    descripcion = db.Column(String(256))
    importe_unitario = db.Column(Float(asdecimal=True), nullable=False)
    unidad = db.Column(ForeignKey('unidad.id',
                                  onupdate='CASCADE'), nullable=False, index=True)
    ingrediente = db.Column(ForeignKey(
        'ingrediente.id', onupdate='CASCADE'), nullable=False, index=True)

    ingrediente1 = db.relationship('Ingrediente')
    unidad1 = db.relationship('Unidad')

    def __init__(self, nom, desc, imp_unitario, uni, ingred):
        self.nombre = nom
        self.descripcion = desc
        self.importe_unitario = imp_unitario
        self.unidad = uni
        self.ingrediente = ingred
        print('<Producto {}>:{}'.format(self.nombre, self.__dict__))

    def ver(self):
        return '<Product {}>'.format(self.nombre)


class TipoUsuario(db.Model, SerializerMixin):
    __tablename__ = 'tipo_usuario'

    id = db.Column(Integer, primary_key=True)
    descripcion = db.Column(String(120))

    def ver(self):
        return '<User {}>'.format(self.id)

    def __init__(self, desc):
        self.descripcion = desc
        print('<TipoUsuario {}>:{}'.format(self.id, self.__dict__))


class Unidad(db.Model, SerializerMixin):
    __tablename__ = 'unidad'

    id = db.Column(Integer, primary_key=True)
    abreviacion = db.Column(String(10), nullable=False)
    descripcion = db.Column(String(120))

    def ver(self):
        return '<User {}>'.format(self.abreviacion)

    def __init__(self, abre, desc):
        self.abreviacion = abre
        self.descripcion = desc
        print('<Unidad {}>:{}'.format(self.id, self.__dict__))


class Usuario(UserMixin, db.Model, SerializerMixin):
    """Modelo de cuenta de usuario"""

    __tablename__ = 'usuario'

    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(45), nullable=False, unique=True)
    password = db.Column(String(45), nullable=False)
    email = db.Column(String(120), nullable=False, unique=True)
    nombre = db.Column(String(120))
    apellido = db.Column(String(120))
    cuit = db.Column(String(45), unique=True)
    es_usuario = db.Column(Integer)
    dni = db.Column(String(45), unique=True)
    razon_social = db.Column(String(120))
    tipo_usuario = db.Column(ForeignKey(
        'tipo_usuario.id'), nullable=False, index=True)

    tipo_usuario1 = db.relationship('TipoUsuario')

    def __init__(self, username, email, passw, nombre, apellido, cuit, es_usuario, dni, razon, tipo):
        self.password = passw
        self.username = username
        self.email = email
        self.nombre = nombre
        self.apellido = apellido
        self.cuit = cuit
        self.es_usuario = 1
        self.dni = dni
        self.razon_social = razon
        self.tipo_usuario = tipo
        print('<User {}>:{}'.format(self.username, self.__dict__))

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def ver(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


def crear(objeto):
    try:
        db.session.add(objeto)
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return True


def crearMuchos(*objetos):
    try:
        db.session.bulk_save_objects(objetos)
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return True


def borrarTodos(objeto):
    try:
        num_rows_deleted = db.session.query(objeto).delete()
        db.session.commit()
    except:
        db.session.rollback()
        return 0
    return num_rows_deleted


class CabeceraSchema(ma.ModelSchema):
    class Meta:
        model = CabeceraDetalle
        sqla_session = db.session


class HistorialSchema(ma.ModelSchema):
    class Meta:
        model = HistorialStock
        sqla_session = db.session


class IngredienteSchema(ma.ModelSchema):
    class Meta:
        model = Ingrediente
        sqla_session = db.session


class LineaSchema(ma.ModelSchema):
    class Meta:
        model = LineaDetalle
        sqla_session = db.session


class PedidoSchema(ma.ModelSchema):
    class Meta:
        model = Pedido
        sqla_session = db.session


class ProductoSchema(ma.ModelSchema):
    class Meta:
        model = Producto
        sqla_session = db.session


class TipoUsuarioSchema(ma.ModelSchema):
    class Meta:
        model = TipoUsuario
        sqla_session = db.session


class UnidadSchema(ma.ModelSchema):
    class Meta:
        model = Unidad
        sqla_session = db.session


class UsuarioSchema(ma.ModelSchema):
    class Meta:
        model = Usuario
        sqla_session = db.session
