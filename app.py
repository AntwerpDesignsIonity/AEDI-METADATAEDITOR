"""
MAD-STAMP Metadata Editor - Flask Web Application
Provides a web-based GUI for metadata stamping and management
"""

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import os
import json
import shutil
from pathlib import Path
from werkzeug.utils import secure_filename
from metadata_core import MetadataStamp

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TEMP_FOLDER'] = 'temp'

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

# Initialize metadata stamper
stamper = MetadataStamp()

ALLOWED_EXTENSIONS = set([
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp',
    'mp3', 'mp4', 'm4a', 'flac',
    'pdf', 'txt'
])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Get file info
    file_info = stamper.get_file_info(filepath)
    
    # Try to extract existing metadata
    existing_metadata = stamper.extract_metadata(filepath)
    
    return jsonify({
        'success': True,
        'filename': filename,
        'file_info': file_info,
        'existing_metadata': existing_metadata
    })


@app.route('/api/stamp', methods=['POST'])
def stamp_metadata():
    """Stamp metadata onto a file"""
    data = request.get_json()
    
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    # Create metadata
    metadata = stamper.create_metadata(
        title=data.get('title', ''),
        author=data.get('author', ''),
        description=data.get('description', ''),
        tags=data.get('tags', []),
        copyright_info=data.get('copyright', ''),
        custom_fields=data.get('custom', {})
    )
    
    # Stamp the file
    output_path = os.path.join(app.config['TEMP_FOLDER'], 'stamped_' + secure_filename(filename))
    success = stamper.stamp_file(filepath, metadata, output_path)
    
    if success:
        # Move stamped file back to uploads
        shutil.move(output_path, filepath)
        return jsonify({
            'success': True,
            'message': 'Metadata stamped successfully',
            'metadata': metadata
        })
    else:
        return jsonify({'error': 'Failed to stamp metadata'}), 500


@app.route('/api/extract', methods=['POST'])
def extract_metadata():
    """Extract metadata from a file"""
    data = request.get_json()
    
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    metadata = stamper.extract_metadata(filepath)
    
    if metadata:
        return jsonify({
            'success': True,
            'metadata': metadata
        })
    else:
        return jsonify({
            'success': True,
            'metadata': None,
            'message': 'No MAD-STAMP metadata found'
        })


@app.route('/api/remove', methods=['POST'])
def remove_metadata():
    """Remove metadata from a file"""
    data = request.get_json()
    
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    success = stamper.remove_metadata(filepath)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Metadata removed successfully'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Could not remove metadata (may not be supported for this file type)'
        })


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download a processed file"""
    safe_filename = secure_filename(filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=safe_filename)
    else:
        return jsonify({'error': 'File not found'}), 404


@app.route('/api/info')
def get_info():
    """Get application information"""
    return jsonify({
        'name': 'MAD-STAMP Metadata Editor',
        'version': stamper.VERSION,
        'author': 'Johan Wilhelm van Antwerp',
        'supported_formats': {
            'images': stamper.supported_image_formats,
            'audio': stamper.supported_audio_formats,
            'documents': stamper.supported_document_formats
        }
    })


@app.route('/api/clear', methods=['POST'])
def clear_uploads():
    """Clear uploaded files"""
    try:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
        
        return jsonify({
            'success': True,
            'message': 'All files cleared'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import os
    
    print("=" * 60)
    print("MAD-STAMP Metadata Editor")
    print("=" * 60)
    print("Starting web server on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Only enable debug mode in development
    # For production, set DEBUG=False in environment
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
