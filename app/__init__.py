from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate()
migrate.init_app(app, db)

login = LoginManager()
login.init_app(app)
login.login_view = 'preview'
login.login_message = 'You must sign in'

mail = Mail()
mail.init_app(app)

bootstrap = Bootstrap()
bootstrap.init_app(app)


def create_app():
    pass


from app import routes, models, forms
