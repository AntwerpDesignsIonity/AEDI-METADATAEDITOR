# Quick Start Guide - MAD-STAMP Metadata Editor

## Getting Started in 5 Minutes

### Step 1: Setup
```bash
# Clone the repository
git clone https://github.com/AntwerpDesignsIonity/AEDI-METADATAEDITOR.git
cd AEDI-METADATAEDITOR

# Run the setup script
bash setup.sh
```

### Step 2: Start the Application
```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
python app.py
```

### Step 3: Open in Browser
Navigate to: **http://localhost:5000**

### Step 4: Upload and Stamp

1. **Upload a file** - Click the upload area or drag & drop
2. **Fill in metadata**:
   - Title: "My Amazing Photo"
   - Author: "Your Name"
   - Description: "A beautiful sunset photograph"
   - Tags: "sunset, photography, nature"
   - Copyright: "© 2026 Your Name"
3. **Click "Stamp Metadata"** - Done! Your file now has embedded metadata
4. **Download** - Click the download button to get your stamped file

## Example Usage

### Stamping Multiple Files

Use the Python API for batch processing:

```python
from metadata_core import MetadataStamp

stamper = MetadataStamp()

# Create metadata
metadata = stamper.create_metadata(
    title="Vacation Photos 2026",
    author="Your Name",
    tags=["vacation", "travel", "2026"]
)

# Stamp an entire folder
results = stamper.stamp_folder("./my_photos", metadata)

# Check results
for file, success in results.items():
    if success:
        print(f"✅ {file}")
    else:
        print(f"❌ {file}")
```

### Extracting Metadata

```python
from metadata_core import MetadataStamp

stamper = MetadataStamp()

# Extract from a single file
metadata = stamper.extract_metadata("photo.jpg")

if metadata:
    print(f"Title: {metadata['title']}")
    print(f"Author: {metadata['author']}")
    print(f"Tags: {', '.join(metadata['tags'])}")
```

### Custom Metadata Fields

```json
{
  "license": "CC BY-NC-SA 4.0",
  "project": "My Project",
  "client": "Client Name",
  "location": "Cape Town, South Africa",
  "camera": "Canon EOS R5",
  "keywords": ["professional", "commercial"]
}
```

## Supported File Types

✅ **Images**: JPG, PNG, GIF, BMP, TIFF, WebP  
✅ **Audio**: MP3, MP4, M4A, FLAC  
✅ **Documents**: PDF, TXT  
✅ **Others**: Sidecar JSON files

## Tips & Tricks

- **Preserve Originals**: The app creates copies when stamping
- **Batch Processing**: Use Python API for multiple files
- **Custom Fields**: Add any JSON data you need
- **Portable**: Metadata travels with your files
- **Non-Destructive**: Original content remains unchanged

## Troubleshooting

**Port already in use?**
```bash
# Change port in app.py (last line):
app.run(host='0.0.0.0', port=8000, debug=True)
```

**Dependencies missing?**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Upload fails?**
- Check file size (max 50MB)
- Verify file type is supported
- Ensure proper file permissions

## Learn More

- Full documentation: `USER_GUIDE.md`
- Repository: https://github.com/AntwerpDesignsIonity/AEDI-METADATAEDITOR
- Contact: johan@antwerpdesigns.com
