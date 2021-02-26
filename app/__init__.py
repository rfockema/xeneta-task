from flask import Flask

from app.models import db
from app.views import main

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.cfg')
    db.init_app(app)
    app.register_blueprint(main)
    return app

app = create_app()