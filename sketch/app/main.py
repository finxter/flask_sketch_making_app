import cv2
import os
from werkzeug.utils import secure_filename
from flask import request, render_template
from app import app
from app.file import allowed_file
from app.sketch import make_sketch



UPLOAD_FOLDER = 'app/static/uploads'
SKETCH_FOLDER = 'app/static/sketches'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sketch', methods=['GET', 'POST'])
def sketch():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename =secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = cv2.imread(UPLOAD_FOLDER+'/'+filename)
        sketch_img = make_sketch(img)
        sketch_img_name = filename.split('.')[0]+'_sketch.jpg'
        save = cv2.imwrite(SKETCH_FOLDER+'/'+sketch_img_name, sketch_img)
        return render_template('home.html', org_img_name=filename, sketch_img_name=sketch_img_name)
    return render_template('home.html')
