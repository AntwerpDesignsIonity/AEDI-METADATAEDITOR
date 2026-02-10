# MAD-STAMP Metadata Editor - Features & Capabilities

## Core Features

### 1. Metadata Stamping (Injection)
- Embed metadata directly into files using industry-standard methods
- Supports multiple file types with type-specific encoding
- Base64 encoding for secure, portable metadata
- Preserves original file content and structure
- Non-destructive stamping process

### 2. Metadata Viewing (Extraction)
- Extract embedded MAD-STAMP metadata from files
- Display metadata in human-readable format
- View raw JSON data for debugging
- Automatic detection of metadata presence
- Support for various metadata formats

### 3. Metadata Management
- Add, edit, and update metadata fields
- Remove metadata when needed
- Batch processing for folders
- Custom field support via JSON
- Standardized metadata structure

### 4. Web-Based GUI
- Modern, responsive HTML/CSS/JavaScript interface
- Drag-and-drop file upload
- Real-time status updates
- Clean, intuitive design
- Mobile-friendly layout

### 5. Python Backend
- Flask web server
- RESTful API endpoints
- Virtual environment isolation
- Extensible core library
- Command-line support

## Supported File Types

### Images
- **PNG** - Uses PNG text chunks for metadata storage
- **JPEG/JPG** - Uses EXIF data fields
- **GIF** - EXIF-based metadata
- **BMP** - EXIF-based metadata
- **TIFF** - EXIF-based metadata
- **WebP** - EXIF-based metadata

### Audio Files
- **MP3** - Uses ID3 tags (EasyID3)
- **MP4/M4A** - Uses MP4 metadata atoms
- **FLAC** - Uses Vorbis comments

### Documents
- **PDF** - Uses PDF metadata dictionary
- **TXT** - Prepends metadata as comment

### Other Files
- Automatically creates sidecar `.mad-metadata.json` files
- Supports any file type through sidecar system

## Metadata Fields

### Standard Fields
- **Title** - File or content title
- **Author** - Creator/author name
- **Description** - Detailed description
- **Tags** - Array of keywords/tags
- **Copyright** - Copyright information
- **Timestamp** - Auto-generated creation timestamp
- **Version** - MAD-STAMP version number

### Custom Fields
- **JSON-based** - Any additional fields via JSON
- **Flexible** - No restrictions on field names
- **Nested** - Support for complex data structures
- **Type-safe** - Proper JSON validation

### Example Metadata Structure
```json
{
  "mad_stamp_version": "1.0.0",
  "timestamp": "2026-02-10T13:40:22.145852",
  "title": "My Document",
  "author": "Creator Name",
  "description": "Document description",
  "tags": ["tag1", "tag2", "tag3"],
  "copyright": "© 2026 Copyright Holder",
  "custom": {
    "license": "CC BY-NC-SA 4.0",
    "project": "Project Name",
    "client": "Client Name",
    "any_field": "any_value"
  }
}
```

## API Endpoints

### File Operations
- `POST /api/upload` - Upload a file
- `POST /api/stamp` - Stamp metadata onto file
- `POST /api/extract` - Extract metadata from file
- `POST /api/remove` - Remove metadata from file
- `GET /api/download/<filename>` - Download processed file
- `POST /api/clear` - Clear all uploaded files

### Information
- `GET /api/info` - Get application information
- Returns supported formats and version info

## Security Features

### File Handling
- Secure filename sanitization
- File type validation
- Size limit enforcement (50MB default)
- Temporary file isolation
- Upload folder separation

### Metadata Protection
- Base64 encoding for data integrity
- Non-removable without deliberate extraction
- Maintains file integrity
- Version tracking
- Timestamp verification

## Advanced Usage

### Python API
```python
from metadata_core import MetadataStamp

stamper = MetadataStamp()

# Create metadata
metadata = stamper.create_metadata(
    title="Example",
    author="Your Name"
)

# Stamp file
stamper.stamp_file("input.jpg", metadata, "output.jpg")

# Extract metadata
data = stamper.extract_metadata("output.jpg")

# Stamp entire folder
results = stamper.stamp_folder("/path/to/folder", metadata)
```

### Batch Processing
- Process multiple files at once
- Folder-level operations
- Result tracking for each file
- Error handling per file
- Progress monitoring

### Integration
- Standalone library (`metadata_core.py`)
- Flask web service
- Command-line interface
- Python package compatible
- REST API for external tools

## Use Cases

### Creative Professionals
- Photographers: Embed copyright and EXIF data
- Designers: Track project information
- Artists: Protect intellectual property
- Musicians: Audio file metadata management

### Organizations
- Document management systems
- Digital asset management
- Content tracking
- License management
- Audit trails

### Developers
- Automated metadata stamping
- Content management systems
- File processing pipelines
- Integration with existing tools

## Technical Specifications

### Dependencies
- Flask 3.0.0 - Web framework
- Pillow 10.2.0 - Image processing
- PyPDF2 3.0.1 - PDF handling
- Mutagen 1.47.0 - Audio metadata
- Python 3.8+ - Runtime

### Performance
- Fast metadata injection
- Minimal file size increase
- Efficient Base64 encoding
- Optimized for batch processing
- Low memory footprint

### Compatibility
- Cross-platform (Windows, Linux, macOS)
- Python 3.8+
- Modern web browsers
- No external database required
- Portable installation

## Limitations & Considerations

### Current Limitations
- Image metadata removal limited to some formats
- Audio/document removal requires specialized handling
- 50MB file size limit (configurable)
- Development server (not production-ready as-is)

### Best Practices
- Always keep original files
- Test on copies first
- Verify metadata after stamping
- Use version control
- Regular backups

### Future Enhancements
- Production WSGI server support
- Enhanced removal capabilities
- More file format support
- Batch upload interface
- User authentication
- Cloud storage integration

## License & Credits

**License**: Creative Commons 4.0 BY-NC-SA
- Free for personal and non-commercial use
- Commercial use requires licensing

**Creator**: Johan Wilhelm van Antwerp  
**Project**: Antwerp Designs, Ionity, Project Alpha  
**ORCID**: 0009-0005-7181-0347

## Support & Resources

- **Email**: johan@antwerpdesigns.com
- **Repository**: https://github.com/AntwerpDesignsIonity/AEDI-METADATAEDITOR
- **Documentation**: See `USER_GUIDE.md` and `QUICKSTART.md`
- **License Info**: See `LICENSE` file
