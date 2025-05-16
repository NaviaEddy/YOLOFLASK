import os
from flask import Blueprint, render_template, request, current_app
from werkzeug.utils import secure_filename
from services.yolo_service import detect_humans

Extesiones = {'png', 'jpg', 'jpeg'}

routes = Blueprint('routes', __name__) #Le digo a Flask que voy a crear un blueprint de rutas

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Extesiones #Me devuelve True si la extension es correcta

@routes.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No hay un archivo seleccionado')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No hay un archivo seleccionado')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            #Guardamos la imagen recibida
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            #Detecciones
            humans, output_path  = detect_humans(save_path)
            rel_output = '/static/uploads/' + os.path.basename(output_path)
            return render_template('result.html', humans=humans, image_path=rel_output)
    return render_template('index.html')



    