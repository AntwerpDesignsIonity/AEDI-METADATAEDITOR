# MAD-STAMP Metadata Editor - User Guide

## Overview

MAD-STAMP (Metadata Antwerp Designs - STAMP) is a powerful, web-based metadata editor that allows you to embed, view, and manage metadata in various file types while preserving file integrity.

## Features

- ✨ **Metadata Injection**: Stamp files with custom metadata
- 🔍 **Metadata Viewing**: Extract and view existing metadata
- 🗑️ **Metadata Removal**: Remove metadata when needed
- 📁 **Multiple File Types**: Support for images, audio, documents
- 🌐 **Web Interface**: Easy-to-use HTML GUI
- 🐍 **Python-based**: Runs locally in a virtual environment
- 🔒 **Secure**: Base64 encoding for metadata preservation

## Supported File Formats

### Images
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

### Audio
- MP3 (.mp3)
- MP4 Audio (.mp4, .m4a)
- FLAC (.flac)

### Documents
- PDF (.pdf)
- Text Files (.txt)

### Other Files
For unsupported file types, metadata is stored in a sidecar JSON file.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository** (or navigate to the project directory):
```bash
cd /path/to/AEDI-METADATAEDITOR
```

2. **Run the setup script**:
```bash
bash setup.sh
```

This script will:
- Create a Python virtual environment
- Install all required dependencies
- Prepare the application for use

3. **Activate the virtual environment**:
```bash
source venv/bin/activate
```

4. **Start the application**:
```bash
python app.py
```

5. **Open your browser** and navigate to:
```
http://localhost:5000
```

## Usage Guide

### 1. Upload a File

- Click on the upload area or drag and drop a file
- Supported files will be uploaded automatically
- File information will be displayed

### 2. Add Metadata

Fill in the metadata fields:

- **Title**: Name or title of the content
- **Author**: Creator or author name
- **Description**: Detailed description of the content
- **Tags**: Comma-separated keywords (e.g., "art, photography, nature")
- **Copyright**: Copyright information (e.g., "© 2026 Your Name")
- **Custom Fields**: Additional metadata in JSON format

Example custom fields:
```json
{
  "license": "CC BY-NC-SA 4.0",
  "project": "Project Alpha",
  "category": "Digital Art"
}
```

### 3. Stamp Metadata

- Click the **"✨ Stamp Metadata"** button
- The file will be processed with the embedded metadata
- Success message will be displayed
- Metadata will be shown in the display section

### 4. View Existing Metadata

- Upload a file that already has metadata
- Click the **"🔍 View Existing Metadata"** button
- Metadata will be extracted and displayed

### 5. Remove Metadata

- Upload a file with metadata
- Click the **"🗑️ Remove Metadata"** button
- Confirm the action
- Metadata will be removed from the file

### 6. Download Processed File

- After stamping metadata, the **"⬇️ Download File"** button appears
- Click to download the processed file with embedded metadata

## How It Works

### Metadata Encoding

MAD-STAMP uses a robust metadata encoding system:

1. **JSON Structure**: Metadata is organized in a JSON format
2. **Base64 Encoding**: The JSON is encoded to Base64
3. **Marker System**: A unique marker identifies MAD-STAMP metadata
4. **File Integration**: Metadata is embedded using file-type-specific methods

### File-Type Specific Methods

- **PNG Images**: Uses PNG text chunks
- **JPEG/Other Images**: Uses EXIF data fields
- **MP3 Audio**: Uses ID3 tags
- **MP4/M4A Audio**: Uses MP4 metadata atoms
- **FLAC Audio**: Uses Vorbis comments
- **PDF Documents**: Uses PDF metadata dictionary
- **Text Files**: Prepends metadata as a comment
- **Other Files**: Creates a `.mad-metadata.json` sidecar file

### Metadata Structure

```json
{
  "mad_stamp_version": "1.0.0",
  "timestamp": "2026-02-10T13:34:32.000000",
  "title": "Example Title",
  "author": "Johan Wilhelm van Antwerp",
  "description": "Example description",
  "tags": ["example", "metadata", "test"],
  "copyright": "© 2026 Antwerp Designs",
  "custom": {
    "license": "CC BY-NC-SA 4.0",
    "project": "MAD-STAMP"
  }
}
```

## API Endpoints

The application provides several REST API endpoints:

- `POST /api/upload` - Upload a file
- `POST /api/stamp` - Stamp metadata onto a file
- `POST /api/extract` - Extract metadata from a file
- `POST /api/remove` - Remove metadata from a file
- `GET /api/download/<filename>` - Download a processed file
- `GET /api/info` - Get application information
- `POST /api/clear` - Clear all uploaded files

## Troubleshooting

### Common Issues

1. **File Upload Fails**
   - Check that the file type is supported
   - Ensure file size is under 50MB
   - Verify file is not corrupted

2. **Metadata Not Stamped**
   - Some file formats may not support all metadata fields
   - Check console for error messages
   - Try a different file format

3. **Cannot Extract Metadata**
   - File may not have MAD-STAMP metadata
   - File may have been processed with a different tool
   - Metadata may have been stripped by another application

4. **Application Won't Start**
   - Ensure Python 3.8+ is installed
   - Verify virtual environment is activated
   - Check that all dependencies are installed: `pip install -r requirements.txt`
   - Ensure port 5000 is not in use

## Security Considerations

- Files are stored temporarily in the `uploads/` folder
- Uploaded files are automatically secured with `secure_filename()`
- Maximum file size is limited to 50MB
- The application runs on localhost by default
- **Debug mode is disabled by default** for security
  - Enable debug mode only in development: `DEBUG=true python app.py`
- For production use, configure:
  - Proper authentication and HTTPS
  - A production WSGI server (e.g., Gunicorn, uWSGI)
  - Firewall rules and access controls
  - Regular security updates

## Advanced Usage

### Batch Processing

For processing multiple files, you can use the Python API directly:

```python
from metadata_core import MetadataStamp

stamper = MetadataStamp()

# Create metadata
metadata = stamper.create_metadata(
    title="Batch Process",
    author="Your Name",
    tags=["batch", "processing"]
)

# Stamp a folder
results = stamper.stamp_folder("/path/to/folder", metadata)

# Check results
for filepath, success in results.items():
    print(f"{filepath}: {'Success' if success else 'Failed'}")
```

### Custom Integration

You can integrate the metadata core library into your own Python applications:

```python
from metadata_core import MetadataStamp

stamper = MetadataStamp()

# Stamp a single file
metadata = stamper.create_metadata(
    title="My Document",
    author="Me",
    description="Important document"
)

stamper.stamp_file("document.pdf", metadata, "document_stamped.pdf")

# Extract metadata
extracted = stamper.extract_metadata("document_stamped.pdf")
print(extracted)
```

## License

Creative Commons 4.0 BY-NC-SA

- Free for personal and non-commercial use
- For commercial use, contact Antwerp Designs at info@antwerpdesigns.com
- All rights reserved | TM² | CC | 2018-2026

## Support

For questions, issues, or commercial licensing:

- Email: johan@antwerpdesigns.com
- Email: johan@ionityearth.shop
- Phone: +27 75 411 0887 (ZAR)

## Credits

**Created by**: Johan Wilhelm van Antwerp  
**ORCID**: 0009-0005-7181-0347  
**Project**: Antwerp Designs, Ionity, Project Alpha  
**Location**: Pretoria & Centurion, Gauteng, South Africa

## Version History

- **v1.0.0** (2026-02-10): Initial release
  - Web-based GUI interface
  - Support for images, audio, and documents
  - Metadata stamping, extraction, and removal
  - Python virtual environment setup
  - Base64 metadata encoding
