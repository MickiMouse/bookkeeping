from flask import Blueprint

bp = Blueprint('card', __name__)

from app.card import routes
