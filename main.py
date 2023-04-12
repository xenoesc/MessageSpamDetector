# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from analysis import analyse

# Create a Flask instance
app = Flask(__name__)

# Define upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define a route for uploading files and handling GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # Handle POST request
    if request.method == 'POST':
        # Delete the contents of the uploads folder
        folder = app.config['UPLOAD_FOLDER']
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # If user does not select file, browser also submit an empty part without filename
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # Save the file and redirect to the result page
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('result', filename=filename))
    # Handle GET request by rendering the upload page
    return render_template('index.html')

# Define a route for showing the result of the analysis
@app.route('/result/<filename>')
def result(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    gauge_value = analyse(file_path) # Call external function
    return render_template('display.html', filename=filename, gauge_value=gauge_value)

# Define a route for serving uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Run the app if this is the main module
if __name__ == '__main__':
    app.run(debug=True)
