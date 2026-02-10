"""
MAD-STAMP Metadata Editor Core Library
Handles metadata injection, extraction, and management for various file types
"""

import os
import json
import base64
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import PyPDF2
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC


class MetadataStamp:
    """Core class for metadata stamping and management"""
    
    METADATA_MARKER = "MAD-STAMP-METADATA"
    VERSION = "1.0.0"
    
    def __init__(self):
        self.supported_image_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        self.supported_audio_formats = ['.mp3', '.mp4', '.m4a', '.flac']
        self.supported_document_formats = ['.pdf', '.txt']
        
    def create_metadata(self, 
                       title: str = "",
                       author: str = "",
                       description: str = "",
                       tags: List[str] = None,
                       copyright_info: str = "",
                       custom_fields: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a metadata dictionary"""
        
        metadata = {
            "mad_stamp_version": self.VERSION,
            "timestamp": datetime.now().isoformat(),
            "title": title,
            "author": author,
            "description": description,
            "tags": tags or [],
            "copyright": copyright_info,
            "custom": custom_fields or {}
        }
        
        return metadata
    
    def encode_metadata(self, metadata: Dict[str, Any]) -> str:
        """Encode metadata to Base64 string"""
        json_str = json.dumps(metadata, indent=2)
        encoded = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        return f"{self.METADATA_MARKER}:{encoded}"
    
    def decode_metadata(self, encoded_str: str) -> Optional[Dict[str, Any]]:
        """Decode metadata from Base64 string"""
        try:
            if encoded_str.startswith(self.METADATA_MARKER + ":"):
                encoded_data = encoded_str.split(":", 1)[1]
                decoded = base64.b64decode(encoded_data).decode('utf-8')
                return json.loads(decoded)
        except Exception as e:
            print(f"Error decoding metadata: {e}")
        return None
    
    def get_file_type(self, filepath: str) -> str:
        """Determine the file type based on extension"""
        ext = Path(filepath).suffix.lower()
        
        if ext in self.supported_image_formats:
            return 'image'
        elif ext in self.supported_audio_formats:
            return 'audio'
        elif ext in self.supported_document_formats:
            return 'document'
        else:
            return 'other'
    
    def stamp_image(self, image_path: str, metadata: Dict[str, Any], output_path: str = None) -> bool:
        """Stamp metadata onto an image file"""
        try:
            if output_path is None:
                output_path = image_path
            
            encoded_metadata = self.encode_metadata(metadata)
            ext = Path(image_path).suffix.lower()
            
            img = Image.open(image_path)
            
            if ext == '.png':
                # PNG supports text chunks
                pnginfo = PngInfo()
                pnginfo.add_text("MAD-STAMP", encoded_metadata)
                pnginfo.add_text("Title", metadata.get("title", ""))
                pnginfo.add_text("Author", metadata.get("author", ""))
                pnginfo.add_text("Description", metadata.get("description", ""))
                img.save(output_path, pnginfo=pnginfo)
            else:
                # For other formats, use EXIF data
                exif_data = img.getexif()
                # User Comment tag (0x9286)
                exif_data[0x9286] = encoded_metadata
                img.save(output_path, exif=exif_data)
            
            return True
        except Exception as e:
            print(f"Error stamping image: {e}")
            return False
    
    def extract_image_metadata(self, image_path: str) -> Optional[Dict[str, Any]]:
        """Extract metadata from an image file"""
        try:
            img = Image.open(image_path)
            ext = Path(image_path).suffix.lower()
            
            if ext == '.png':
                # Check PNG text chunks
                if hasattr(img, 'text') and 'MAD-STAMP' in img.text:
                    return self.decode_metadata(img.text['MAD-STAMP'])
            else:
                # Check EXIF data
                exif_data = img.getexif()
                if exif_data and 0x9286 in exif_data:
                    return self.decode_metadata(exif_data[0x9286])
            
            return None
        except Exception as e:
            print(f"Error extracting image metadata: {e}")
            return None
    
    def stamp_audio(self, audio_path: str, metadata: Dict[str, Any], output_path: str = None) -> bool:
        """Stamp metadata onto an audio file"""
        try:
            if output_path is None:
                output_path = audio_path
            
            encoded_metadata = self.encode_metadata(metadata)
            ext = Path(audio_path).suffix.lower()
            
            if ext == '.mp3':
                audio = MP3(audio_path, ID3=EasyID3)
                if audio.tags is None:
                    audio.add_tags()
                audio.tags['title'] = metadata.get('title', '')
                audio.tags['artist'] = metadata.get('author', '')
                audio.tags['comment'] = encoded_metadata
                audio.save()
            elif ext in ['.mp4', '.m4a']:
                audio = MP4(audio_path)
                audio.tags['\xa9nam'] = metadata.get('title', '')
                audio.tags['\xa9ART'] = metadata.get('author', '')
                audio.tags['\xa9cmt'] = encoded_metadata
                audio.save()
            elif ext == '.flac':
                audio = FLAC(audio_path)
                audio['title'] = metadata.get('title', '')
                audio['artist'] = metadata.get('author', '')
                audio['comment'] = encoded_metadata
                audio.save()
            
            return True
        except Exception as e:
            print(f"Error stamping audio: {e}")
            return False
    
    def extract_audio_metadata(self, audio_path: str) -> Optional[Dict[str, Any]]:
        """Extract metadata from an audio file"""
        try:
            ext = Path(audio_path).suffix.lower()
            
            if ext == '.mp3':
                audio = MP3(audio_path, ID3=EasyID3)
                if audio.tags and 'comment' in audio.tags:
                    return self.decode_metadata(audio.tags['comment'][0])
            elif ext in ['.mp4', '.m4a']:
                audio = MP4(audio_path)
                if '\xa9cmt' in audio.tags:
                    return self.decode_metadata(audio.tags['\xa9cmt'][0])
            elif ext == '.flac':
                audio = FLAC(audio_path)
                if 'comment' in audio:
                    return self.decode_metadata(audio['comment'][0])
            
            return None
        except Exception as e:
            print(f"Error extracting audio metadata: {e}")
            return None
    
    def stamp_document(self, doc_path: str, metadata: Dict[str, Any], output_path: str = None) -> bool:
        """Stamp metadata onto a document file"""
        try:
            if output_path is None:
                output_path = doc_path
            
            encoded_metadata = self.encode_metadata(metadata)
            ext = Path(doc_path).suffix.lower()
            
            if ext == '.pdf':
                # Read PDF
                reader = PyPDF2.PdfReader(doc_path)
                writer = PyPDF2.PdfWriter()
                
                # Copy pages
                for page in reader.pages:
                    writer.add_page(page)
                
                # Add metadata
                writer.add_metadata({
                    '/Title': metadata.get('title', ''),
                    '/Author': metadata.get('author', ''),
                    '/Subject': metadata.get('description', ''),
                    '/MAD-STAMP': encoded_metadata
                })
                
                # Write output
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
            elif ext == '.txt':
                # For text files, prepend metadata as comment
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                metadata_comment = f"# {encoded_metadata}\n"
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(metadata_comment + content)
            
            return True
        except Exception as e:
            print(f"Error stamping document: {e}")
            return False
    
    def extract_document_metadata(self, doc_path: str) -> Optional[Dict[str, Any]]:
        """Extract metadata from a document file"""
        try:
            ext = Path(doc_path).suffix.lower()
            
            if ext == '.pdf':
                reader = PyPDF2.PdfReader(doc_path)
                if reader.metadata and '/MAD-STAMP' in reader.metadata:
                    return self.decode_metadata(reader.metadata['/MAD-STAMP'])
            elif ext == '.txt':
                with open(doc_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('# ') and self.METADATA_MARKER in first_line:
                        encoded = first_line[2:]
                        return self.decode_metadata(encoded)
            
            return None
        except Exception as e:
            print(f"Error extracting document metadata: {e}")
            return None
    
    def stamp_file(self, filepath: str, metadata: Dict[str, Any], output_path: str = None) -> bool:
        """Stamp metadata onto any supported file"""
        file_type = self.get_file_type(filepath)
        
        if file_type == 'image':
            return self.stamp_image(filepath, metadata, output_path)
        elif file_type == 'audio':
            return self.stamp_audio(filepath, metadata, output_path)
        elif file_type == 'document':
            return self.stamp_document(filepath, metadata, output_path)
        else:
            # For unsupported file types, create a sidecar file
            if output_path is None:
                output_path = filepath
            sidecar_path = output_path + '.mad-metadata.json'
            try:
                with open(sidecar_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                return True
            except Exception as e:
                print(f"Error creating sidecar metadata: {e}")
                return False
    
    def extract_metadata(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Extract metadata from any supported file"""
        file_type = self.get_file_type(filepath)
        
        if file_type == 'image':
            return self.extract_image_metadata(filepath)
        elif file_type == 'audio':
            return self.extract_audio_metadata(filepath)
        elif file_type == 'document':
            return self.extract_document_metadata(filepath)
        else:
            # Check for sidecar file
            sidecar_path = filepath + '.mad-metadata.json'
            if os.path.exists(sidecar_path):
                try:
                    with open(sidecar_path, 'r') as f:
                        return json.load(f)
                except Exception as e:
                    print(f"Error reading sidecar metadata: {e}")
            return None
    
    def remove_metadata(self, filepath: str, output_path: str = None) -> bool:
        """Remove MAD-STAMP metadata from a file"""
        try:
            if output_path is None:
                output_path = filepath
            
            file_type = self.get_file_type(filepath)
            
            if file_type == 'image':
                img = Image.open(filepath)
                # Save without EXIF/metadata
                img.save(output_path)
                return True
            elif file_type in ['audio', 'document']:
                # For audio and documents, metadata removal requires more complex handling
                # Not currently implemented
                return False
            else:
                # Remove sidecar file if exists
                sidecar_path = filepath + '.mad-metadata.json'
                if os.path.exists(sidecar_path):
                    os.remove(sidecar_path)
                    return True
            
            return False
        except Exception as e:
            print(f"Error removing metadata: {e}")
            return False
    
    def stamp_folder(self, folder_path: str, metadata: Dict[str, Any]) -> Dict[str, bool]:
        """Stamp metadata onto all files in a folder"""
        results = {}
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    success = self.stamp_file(filepath, metadata)
                    results[filepath] = success
                except Exception as e:
                    print(f"Error stamping {filepath}: {e}")
                    results[filepath] = False
        
        return results
    
    def get_file_info(self, filepath: str) -> Dict[str, Any]:
        """Get detailed file information"""
        stat = os.stat(filepath)
        
        return {
            'filename': os.path.basename(filepath),
            'path': filepath,
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'type': self.get_file_type(filepath),
            'extension': Path(filepath).suffix.lower()
        }
