from flask import Flask, jsonify, request, render_template_string
import os
import shutil

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
    
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    return jsonify({
        'message': f'File {file.filename} uploaded successfully!',
        'download_url': f'/files/{file.filename}'
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
