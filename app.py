from flask import Flask, request, redirect, url_for, render_template, send_from_directory, abort
import os

app = Flask(__name__, static_folder='.', template_folder='.')

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 54 * 1024 * 1024  # 16 MB limit
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'pdf', 'txt', 'csv', 'exe', 'ico' , 'ipa', 'mov', 'mp4' , 'apk' }  # Allowed file types

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/')
    else:
        return "File type not allowed", 400

@app.route('/download/<filename>')
def download_file(filename):
    # Send the file as an attachment to force download
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/preview/<filename>')
def preview_file(filename):
    # Ensure the file exists
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.isfile(file_path):
        abort(404)
    
    # Check file extension to serve previewable files
    previewable_extensions = {'jpg', 'jpeg', 'png', 'gif', 'pdf', 'mov', 'mp4', 'docx' , 'ico' , 'txt' , 'pdf' }
    file_extension = filename.rsplit('.', 1)[1].lower()
    
    if file_extension in previewable_extensions:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return "File type not previewable", 400

@app.route('/delete', methods=['POST'])
def delete_file():
    filename = request.form.get('filename')
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/')
    except FileNotFoundError:
        return "File not found", 404

# Serve static files from the same directory
@app.route('/<path:filename>')
def serve_static(filename):
    if os.path.isfile(filename):
        return send_from_directory('.', filename)
    abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
