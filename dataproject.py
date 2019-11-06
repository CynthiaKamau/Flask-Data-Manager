from application import app, db
from application.models import User,Sample

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User':User, 'Sample': Sample}