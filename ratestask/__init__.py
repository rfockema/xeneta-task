from flask import Flask

from ratestask.models import db
from ratestask.views import main

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.cfg')
    db.init_app(app)
    app.register_blueprint(main)
    return app
