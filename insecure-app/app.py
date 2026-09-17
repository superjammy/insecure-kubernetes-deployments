from flask import Flask, request, render_template_string, send_from_directory
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    if request.method == 'POST':
        # Arbitrary command execution endpoint removed to prevent unauthenticated remote code execution
        if 'file' in request.files:
            uploaded_file = request.files['file']
            uploaded_file.save(os.path.join('/uploads', uploaded_file.filename))
            output = f"File {uploaded_file.filename} uploaded successfully!"

    return render_template_string("""
        <h1>Intentionally Insecure App</h1>
        <form action="/" method="post" enctype="multipart/form-data">
            Upload a file: <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
        <pre>{{output}}</pre>
    """, output=output)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
