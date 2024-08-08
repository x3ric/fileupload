import os
import socket
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
port = 5000

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_files(directory):
    """Retrieve a list of filenames in the specified directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def is_safe_filename(filename):
    """Check if the filename contains only allowed characters."""
    allowed_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.'
    return all(char in allowed_characters for char in filename)

def get_public_ip():
    """Retrieve the public IP address of the server."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return 'localhost'

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle both GET and POST requests for the file upload form."""
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No selected file')
        filename = secure_filename(file.filename)
        if not is_safe_filename(filename):
            return render_template('index.html', error='Filename contains invalid characters')
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        os.chmod(file_path, 0o644)
    scheme = 'https' if request.is_secure else 'http'
    public_ip = get_public_ip()
    upload_url = f"{scheme}://{public_ip}:{port}/"
    files = get_files(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files, upload_url=upload_url)

@app.route('/download/<filename>')
def download_file(filename):
    """Provide a file for download."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=False, host=get_public_ip(), port=port)
