from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from multiprocessing import Process
from analysis import analyse

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # delete the contents of the uploads folder
        folder = app.config['UPLOAD_FOLDER']
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('result', filename=filename))
    return render_template('index.html')

def analyse_and_set_gauge(filename):
    # This function runs the analyse function and sets the gauge_value
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    global gauge_value

    gauge_value = analyse(filepath)

@app.route('/result/<filename>')
def result(filename):
    global gauge_value
    gauge_value = None
    # create a new process to run analyse_and_set_gauge
    p = Process(target=analyse_and_set_gauge, args=(filename,))
    p.start()
    # display the upload.html template while analyse is running
    return render_template('upload.html')

@app.route('/display')
def display():
    global gauge_value
    if gauge_value is None:
        return redirect(url_for('upload_file'))
    else:
        return render_template('display.html', gauge_value=gauge_value)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
