from application import app, db
from application.models import Users,Sample

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users':Users, 'Sample': Sample}