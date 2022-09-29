from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, SubmitField, StringField #wtforms es una librería que se integra con Python
from wtforms.validators import DataRequired, Length

class MovementForm(FlaskForm):
    date = DateField("Fecha", validators=[DataRequired()])
    description = StringField("Descripción", validators=[DataRequired(), Length(min=3, max=15, message="Mínimo 3 caracteres")])
    quantity = FloatField("Cantidad", validators=[DataRequired()])

    submit = SubmitField("Aceptar")
