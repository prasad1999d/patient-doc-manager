from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import sqlite3
from datetime import datetime
import uuid
import jwt

# Configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
SECRET_KEY = 'your_secret_key'  # Replace in production

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Flask setup
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

DB_PATH = 'filemeta.db'

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    filename TEXT,
                    storage_path TEXT,
                    patient_id TEXT,
                    upload_date TEXT,
                    size_kb INTEGER
                )''')
    conn.commit()
    conn.close()

init_db()

# Allowed file check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# JWT token validation decorator
def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')

        # Fallback to query param for download route
        if not token:
            token = request.args.get('token')
            if token:
                token = f'Bearer {token}'

        if not token:
            return jsonify({'error': 'Missing token'}), 401

        try:
            jwt.decode(token.replace('Bearer ', ''), SECRET_KEY, algorithms=['HS256'])
        except Exception:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# 🔐 Login route (mock user)
@app.route('/login', methods=['POST'])
def login():
    user = request.json.get('user', 'demo')
    token = jwt.encode({'user': user}, SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token})

# 📤 Upload route
@app.route('/documents/upload', methods=['POST'])
@token_required
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    patient_id = request.form.get('patient_id')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not patient_id:
        return jsonify({'error': 'Missing patient_id'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    filename = secure_filename(file.filename)
    unique_id = str(uuid.uuid4())
    stored_filename = f"{unique_id}_{filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)
    file.save(file_path)

    size_kb = round(os.path.getsize(file_path) / 1024)
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO documents (id, filename, storage_path, patient_id, upload_date, size_kb)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (unique_id, filename, stored_filename, patient_id, upload_date, size_kb))
    conn.commit()
    conn.close()

    return jsonify({'id': unique_id, 'message': 'Upload successful'})

# 📄 List documents
@app.route('/documents', methods=['GET'])
@token_required
def list_documents():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, filename, patient_id, upload_date, size_kb FROM documents')
    rows = c.fetchall()
    conn.close()

    docs = [
        {
            'id': row[0],
            'filename': row[1],
            'patient_id': row[2],
            'upload_date': row[3],
            'size_kb': row[4]
        } for row in rows
    ]
    return jsonify(docs)

# ⬇️ Download document
@app.route('/documents/<doc_id>/download', methods=['GET'])
@token_required
def download_document(doc_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT storage_path, filename FROM documents WHERE id = ?', (doc_id,))
    row = c.fetchone()
    conn.close()

    if not row:
        return jsonify({'error': 'Document not found'}), 404

    return send_from_directory(app.config['UPLOAD_FOLDER'], row[0], as_attachment=True, download_name=row[1])

# ❌ Delete document
@app.route('/documents/<doc_id>', methods=['DELETE'])
@token_required
def delete_document(doc_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT storage_path FROM documents WHERE id = ?', (doc_id,))
    row = c.fetchone()

    if not row:
        conn.close()
        return jsonify({'error': 'Document not found'}), 404

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], row[0])
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass  # Already deleted

    c.execute('DELETE FROM documents WHERE id = ?', (doc_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Document deleted'})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200


# 🚀 Run Flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
