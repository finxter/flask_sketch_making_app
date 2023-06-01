import cv2
import os
from werkzeug.utils import secure_filename
from flask import request, render_template
from app import app
from app.file import allowed_file
from app.sketch import make_sketch
from app.cartoonify import cartoon


UPLOAD_FOLDER = 'app/static/uploads'
IMG_FOLDER = 'app/static/images'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sketch', methods=['GET', 'POST'])
def sketch():
    file = request.files['file']
    op = request.form['choice']
    if file and allowed_file(file.filename):
        filename =secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = cv2.imread(UPLOAD_FOLDER+'/'+filename)
        if op == 'sketch':
            sketch_img = make_sketch(img)
            img_name = filename.split('.')[0]+'_sketch.jpg'
            save = cv2.imwrite(IMG_FOLDER+'/'+img_name, sketch_img)
            return render_template('home.html', org_img_name=filename, img_name=img_name)
        else:
            cartoon_img = cartoon(img)
            img_name = filename.split('.')[0]+'_cartoon.jpg'
            save = cv2.imwrite(IMG_FOLDER+'/'+img_name, cartoon_img)
            return render_template('home.html', org_img_name=filename, img_name=img_name)
    return render_template('home.html')
