import os
from flask import Flask
from routes import routes

def create_app():
    app = Flask(__name__)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    updated_folder = os.path.join(base_dir, './static/uploads')
    os.makedirs(updated_folder, exist_ok=True) #Me creas la carpeta si no existe

    app.config['UPLOAD_FOLDER'] = os.path.abspath(updated_folder)

    app.register_blueprint(routes)

    return app