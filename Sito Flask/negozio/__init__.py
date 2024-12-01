from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# importazione del login manager
from flask_login import LoginManager
from flask_migrate import Migrate  

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///negozio.db'
app.config['SECRET_KEY'] = 'ee1441e6d7af920c0ae785f0'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
# inizializzazione del login manager
login_manager = LoginManager(app)
# se non sono loggato forzo di andare al login in caso di pagine protette con messaggio
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from negozio import routes