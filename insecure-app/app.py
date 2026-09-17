from flask import Flask, request, render_template_string, send_from_directory, jsonify
import os
import re
from functools import wraps
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Authentication configuration
API_KEY = os.environ.get('API_KEY', 'default-secure-key-change-in-production')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def require_api_key(f):
    """Decorator to require API key authentication for endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.form.get('api_key')
        if not api_key or api_key != API_KEY:
            return jsonify({'error': 'Unauthorized: Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    if request.method == 'POST':
        # Verify API key for POST requests
        api_key = request.headers.get('X-API-Key') or request.form.get('api_key')
        if not api_key or api_key != API_KEY:
            output = 'Error: Unauthorized. API key required for operations.'
        elif 'command' in request.form:
            # Command execution has been disabled for security reasons
            output = 'Error: Command execution is disabled. This feature has been removed due to security concerns.'
        elif 'file' in request.files:
            uploaded_file = request.files['file']
            if uploaded_file.filename == '':
                output = 'Error: No file selected'
            elif not allowed_file(uploaded_file.filename):
                output = f'Error: File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            else:
                # Sanitize filename to prevent path traversal
                filename = secure_filename(uploaded_file.filename)
                # Validate file size
                uploaded_file.seek(0, os.SEEK_END)
                file_size = uploaded_file.tell()
                if file_size > MAX_FILE_SIZE:
                    output = f'Error: File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024)}MB'
                else:
                    uploaded_file.seek(0)
                    upload_dir = '/uploads'
                    if not os.path.exists(upload_dir):
                        os.makedirs(upload_dir, exist_ok=True)
                    filepath = os.path.join(upload_dir, filename)
                    uploaded_file.save(filepath)
                    output = f"File {filename} uploaded successfully!"

    return render_template_string("""
        <h1>Secure Application</h1>
        <p><strong>Note:</strong> All operations require API key authentication.</p>
        <form action="/" method="post">
            API Key: <input type="password" name="api_key" required>
            <br><br>
            <input type="hidden" name="command" value="disabled">
            <em>Command execution has been disabled for security.</em>
        </form>
        <br>
        <form action="/" method="post" enctype="multipart/form-data">
            API Key: <input type="password" name="api_key" required>
            <br><br>
            Upload a file: <input type="file" name="file" required>
            <input type="submit" value="Upload">
            <br><small>Allowed types: txt, pdf, png, jpg, jpeg, gif (max 10MB)</small>
        </form>
        <pre>{{output}}</pre>
    """, output=output)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
