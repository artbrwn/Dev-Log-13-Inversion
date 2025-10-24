from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Optional

class TradeForm(FlaskForm):
    currency_from = SelectField("Moneda origen", choices=[], validators=[DataRequired()])
    currency_to = SelectField("Moneda destino", choices=[], validators=[DataRequired()])
    amount_from = DecimalField("Cantidad origen", validators=[DataRequired(), NumberRange(min=0)])
    amount_to = DecimalField("Cantidad destino", validators=[Optional()])