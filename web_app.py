from app import app, db
from app.models import User, Card


@app.shell_context_processor
def context():
    return {'db': db, 'User': User, 'Card': Card}
