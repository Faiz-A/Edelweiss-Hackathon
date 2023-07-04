import threading
from flask import Flask
import queue
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
DB_NAME = "databas.db"
socket_thread = None
data_queue = queue.Queue()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'teamHades'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import Options, Underlying, Futures
    #create_database(app)
    with app.app_context():
        db.create_all()


    return app




