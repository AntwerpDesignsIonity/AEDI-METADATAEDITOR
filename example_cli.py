#!/usr/bin/env python3
"""
MAD-STAMP Command Line Example
Demonstrates how to use the metadata core library from command line
"""

import sys
import json
from metadata_core import MetadataStamp

def main():
    stamper = MetadataStamp()
    
    print("=" * 70)
    print("MAD-STAMP Metadata Editor - Command Line Example")
    print("=" * 70)
    
    # Example 1: Stamp a file
    print("\n📝 Example 1: Stamping a file with metadata")
    print("-" * 70)
    
    metadata = stamper.create_metadata(
        title="Command Line Example",
        author="MAD-STAMP System",
        description="This file was stamped using the command line interface",
        tags=["cli", "example", "automated"],
        copyright_info="© 2026 Antwerp Designs",
        custom_fields={
            "processing_method": "CLI",
            "automation": True,
            "batch_id": "CMD-001"
        }
    )
    
    print("Created metadata:")
    print(json.dumps(metadata, indent=2))
    
    # Example 2: Extract metadata
    print("\n\n🔍 Example 2: Extracting metadata from files")
    print("-" * 70)
    
    # Check if we have stamped test files
    import os
    test_files = [
        'test_files/test_image_stamped.png',
        'test_files/test_document_stamped.txt'
    ]
    
    for filepath in test_files:
        if os.path.exists(filepath):
            print(f"\nFile: {filepath}")
            extracted = stamper.extract_metadata(filepath)
            if extracted:
                print(f"  ✅ Title: {extracted.get('title', 'N/A')}")
                print(f"  ✅ Author: {extracted.get('author', 'N/A')}")
                print(f"  ✅ Tags: {', '.join(extracted.get('tags', []))}")
                print(f"  ✅ Timestamp: {extracted.get('timestamp', 'N/A')}")
            else:
                print("  ❌ No metadata found")
        else:
            print(f"\n⚠️  File not found: {filepath}")
    
    # Example 3: File information
    print("\n\n📊 Example 3: Getting file information")
    print("-" * 70)
    
    if os.path.exists('test_files/test_image.png'):
        info = stamper.get_file_info('test_files/test_image.png')
        print(f"Filename: {info['filename']}")
        print(f"Type: {info['type']}")
        print(f"Size: {info['size']} bytes")
        print(f"Extension: {info['extension']}")
        print(f"Modified: {info['modified']}")
    
    # Example 4: Batch processing simulation
    print("\n\n📁 Example 4: Batch processing concept")
    print("-" * 70)
    print("To stamp multiple files:")
    print("""
# Create shared metadata
batch_metadata = stamper.create_metadata(
    title="Project Photos",
    author="Team Name",
    tags=["project", "batch-2026"]
)

# Stamp entire folder
results = stamper.stamp_folder('/path/to/photos', batch_metadata)

# Process results
for filepath, success in results.items():
    if success:
        print(f"✅ Stamped: {filepath}")
    else:
        print(f"❌ Failed: {filepath}")
    """)
    
    print("\n" + "=" * 70)
    print("Examples completed! Check the USER_GUIDE.md for more information.")
    print("=" * 70)

if __name__ == "__main__":
    main()
