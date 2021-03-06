from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistroUsuarioForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[
                           DataRequired(),
                           Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirmar Password', validators=[
                                     DataRequired(),
                                     EqualTo('password')])
    nombre = StringField('Nombre', validators=[
        DataRequired(),
        Length(min=2, max=20)])
    apellido = StringField('Apellido', validators=[
        DataRequired(),
        Length(min=2, max=20)])
    dni = StringField('DNI', validators=[
        DataRequired(),
        Length(min=8, max=15)])
    cuit = StringField('CUIT', validators=[
        DataRequired(),
        Length(min=10, max=15)])
    razon = StringField('Empresa', validators=[
        Length(min=2, max=30)])
    submit = SubmitField('Registrame')


class LoginUsuarioForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Ingresar')

class ContactoForm(FlaskForm):
    contacto = StringField('Nombre/Email', validators=[DataRequired()])
    mensaje = TextAreaField('Mensaje', validators=[DataRequired()])
    submit = SubmitField('Enviar')

#class ProductosForm(FlaskForm):
#    nombre = StringField()
#    descripcion = StringField()
#    importe_unitario = 
#    unidad = 
#    ingrediente = 
