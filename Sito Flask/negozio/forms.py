from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, IntegerField
# importo le classi per la validazione dei dati
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from negozio.models import Utente


class RegisterForm(FlaskForm):

    # regole di validazione custom
    def validate_username(self, username_to_check):
        user = Utente.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Il nome utente è già stato inserito, immetti un nome diverso')

    def validate_email_address(self, email_address_to_check):
        email_address =Utente.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Indirizzo email già inserito, fornire un indirizzo diverso')

    username = StringField(label='Nome utente:',validators=[Length(min=2, max=20), DataRequired()])
    email_address = StringField(label='Indirizzo mail:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Conferma Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Crea Account')

class LoginForm(FlaskForm):
    username = StringField(label='Nome utente:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Entra')

# compravendita
class PurchaseItemForm(FlaskForm):
    qta = IntegerField('qta')
    submit = SubmitField(label='Aggiungi al carrello')

class SellItemForm(FlaskForm):
    qta = IntegerField('qta')
    submit = SubmitField(label='Rimuovi dal carrello')