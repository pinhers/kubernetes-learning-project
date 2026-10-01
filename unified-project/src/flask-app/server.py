from flask import Flask, jsonify, request, render_template_string
import os
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)

# This will be the shared upload directory (same as file server)
UPLOAD_FOLDER = '/shared-uploads'

# HTML template for upload form
UPLOAD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>File Upload</title>
</head>
<body>
    <h1>Upload File to Kubernetes</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    <p><a href="/files">View All Files</a></p>
</body>
</html>
'''

@app.route('/')
def hello():
    return jsonify({"message": "Hello from Flask!!"}), 200

@app.route('/health')
def health():
    return "OK", 200

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template_string(UPLOAD_HTML)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    safe_filename = secure_filename(file.filename)
    if safe_filename == '':
        return jsonify({'error': 'Invalid filename'}), 400
    
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Save file (enforce path remains within upload folder)
    upload_root = os.path.abspath(UPLOAD_FOLDER)
    file_path = os.path.abspath(os.path.join(upload_root, safe_filename))
    if os.path.commonpath([upload_root, file_path]) != upload_root:
        return jsonify({'error': 'Invalid file path'}), 400

    file.save(file_path)
    
    return jsonify({
        'message': f'File {safe_filename} uploaded successfully!',
        'download_url': f'/files/{safe_filename}'
    }), 200

@app.route('/files')
def list_files():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return jsonify({'files': files}), 200
    except FileNotFoundError:
        return jsonify({'files': []}), 200

@app.route('/files/<filename>')
def download_file(filename):
    return jsonify({'message': f'File {filename} would be served by file server'})

if __name__ == '__main__':
    print("Starting Flask server with upload functionality...")
    app.run(host='0.0.0.0', port=5000, debug=True)
