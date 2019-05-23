from app import create_app, db
from app.models import User, Card

app = create_app()


@app.shell_context_processor
def context():
    return {'db': db, 'User': User, 'Card': Card}
