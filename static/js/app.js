// MAD-STAMP Metadata Editor - JavaScript Application

let currentFile = null;
let currentFilename = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    loadAppInfo();
});

function setupEventListeners() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');
    const stampBtn = document.getElementById('stampBtn');
    const extractBtn = document.getElementById('extractBtn');
    const removeBtn = document.getElementById('removeBtn');
    const downloadBtn = document.getElementById('downloadBtn');

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Button clicks
    stampBtn.addEventListener('click', stampMetadata);
    extractBtn.addEventListener('click', extractMetadata);
    removeBtn.addEventListener('click', removeMetadata);
    downloadBtn.addEventListener('click', downloadFile);
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    e.currentTarget.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    currentFile = file;
    showStatus('Uploading file...', 'info');
    
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentFilename = data.filename;
            displayFileInfo(data.file_info);
            
            if (data.existing_metadata) {
                populateMetadataForm(data.existing_metadata);
                showStatus('File uploaded! Existing metadata found.', 'success');
            } else {
                clearMetadataForm();
                showStatus('File uploaded successfully!', 'success');
            }
            
            document.getElementById('metadataSection').classList.remove('hidden');
        } else {
            showStatus(data.error || 'Upload failed', 'error');
        }
    })
    .catch(error => {
        console.error('Upload error:', error);
        showStatus('Upload failed: ' + error.message, 'error');
    });
}

function displayFileInfo(fileInfo) {
    const fileInfoDiv = document.getElementById('fileInfo');
    fileInfoDiv.innerHTML = `
        <h3>📄 File Information</h3>
        <p><strong>Filename:</strong> ${fileInfo.filename}</p>
        <p><strong>Type:</strong> ${fileInfo.type}</p>
        <p><strong>Size:</strong> ${formatFileSize(fileInfo.size)}</p>
        <p><strong>Extension:</strong> ${fileInfo.extension}</p>
        <p><strong>Modified:</strong> ${new Date(fileInfo.modified).toLocaleString()}</p>
    `;
    fileInfoDiv.classList.remove('hidden');
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function populateMetadataForm(metadata) {
    document.getElementById('title').value = metadata.title || '';
    document.getElementById('author').value = metadata.author || '';
    document.getElementById('description').value = metadata.description || '';
    document.getElementById('tags').value = (metadata.tags || []).join(', ');
    document.getElementById('copyright').value = metadata.copyright || '';
    
    if (metadata.custom && Object.keys(metadata.custom).length > 0) {
        document.getElementById('customFields').value = JSON.stringify(metadata.custom, null, 2);
    } else {
        document.getElementById('customFields').value = '';
    }
}

function clearMetadataForm() {
    document.getElementById('title').value = '';
    document.getElementById('author').value = '';
    document.getElementById('description').value = '';
    document.getElementById('tags').value = '';
    document.getElementById('copyright').value = '';
    document.getElementById('customFields').value = '';
}

function getMetadataFromForm() {
    const tags = document.getElementById('tags').value
        .split(',')
        .map(tag => tag.trim())
        .filter(tag => tag.length > 0);
    
    let customFields = {};
    const customFieldsText = document.getElementById('customFields').value.trim();
    if (customFieldsText) {
        try {
            customFields = JSON.parse(customFieldsText);
        } catch (e) {
            showStatus('Invalid JSON in custom fields', 'error');
            return null;
        }
    }
    
    return {
        filename: currentFilename,
        title: document.getElementById('title').value,
        author: document.getElementById('author').value,
        description: document.getElementById('description').value,
        tags: tags,
        copyright: document.getElementById('copyright').value,
        custom: customFields
    };
}

function stampMetadata() {
    if (!currentFilename) {
        showStatus('No file selected', 'error');
        return;
    }
    
    const metadata = getMetadataFromForm();
    if (!metadata) return;
    
    showStatus('Stamping metadata...', 'info');
    
    fetch('/api/stamp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(metadata)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showStatus('✅ Metadata stamped successfully!', 'success');
            displayMetadata(data.metadata);
            document.getElementById('downloadBtn').classList.remove('hidden');
        } else {
            showStatus(data.error || 'Failed to stamp metadata', 'error');
        }
    })
    .catch(error => {
        console.error('Stamp error:', error);
        showStatus('Failed to stamp metadata: ' + error.message, 'error');
    });
}

function extractMetadata() {
    if (!currentFilename) {
        showStatus('No file selected', 'error');
        return;
    }
    
    showStatus('Extracting metadata...', 'info');
    
    fetch('/api/extract', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filename: currentFilename })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.metadata) {
            showStatus('✅ Metadata extracted successfully!', 'success');
            displayMetadata(data.metadata);
        } else {
            showStatus(data.message || 'No metadata found', 'info');
            document.getElementById('metadataDisplay').classList.add('hidden');
        }
    })
    .catch(error => {
        console.error('Extract error:', error);
        showStatus('Failed to extract metadata: ' + error.message, 'error');
    });
}

function removeMetadata() {
    if (!currentFilename) {
        showStatus('No file selected', 'error');
        return;
    }
    
    if (!confirm('Are you sure you want to remove the metadata from this file?')) {
        return;
    }
    
    showStatus('Removing metadata...', 'info');
    
    fetch('/api/remove', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filename: currentFilename })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showStatus('✅ Metadata removed successfully!', 'success');
            clearMetadataForm();
            document.getElementById('metadataDisplay').classList.add('hidden');
        } else {
            showStatus(data.message || 'Failed to remove metadata', 'error');
        }
    })
    .catch(error => {
        console.error('Remove error:', error);
        showStatus('Failed to remove metadata: ' + error.message, 'error');
    });
}

function displayMetadata(metadata) {
    const displayDiv = document.getElementById('metadataDisplay');
    const contentDiv = document.getElementById('metadataContent');
    
    let html = '<div class="metadata-items">';
    
    if (metadata.mad_stamp_version) {
        html += `<div class="metadata-item">
            <strong>MAD-STAMP Version:</strong> ${metadata.mad_stamp_version}
        </div>`;
    }
    
    if (metadata.timestamp) {
        html += `<div class="metadata-item">
            <strong>Timestamp:</strong> ${new Date(metadata.timestamp).toLocaleString()}
        </div>`;
    }
    
    if (metadata.title) {
        html += `<div class="metadata-item">
            <strong>Title:</strong> ${escapeHtml(metadata.title)}
        </div>`;
    }
    
    if (metadata.author) {
        html += `<div class="metadata-item">
            <strong>Author:</strong> ${escapeHtml(metadata.author)}
        </div>`;
    }
    
    if (metadata.description) {
        html += `<div class="metadata-item">
            <strong>Description:</strong> ${escapeHtml(metadata.description)}
        </div>`;
    }
    
    if (metadata.tags && metadata.tags.length > 0) {
        html += `<div class="metadata-item">
            <strong>Tags:</strong> ${metadata.tags.map(tag => escapeHtml(tag)).join(', ')}
        </div>`;
    }
    
    if (metadata.copyright) {
        html += `<div class="metadata-item">
            <strong>Copyright:</strong> ${escapeHtml(metadata.copyright)}
        </div>`;
    }
    
    if (metadata.custom && Object.keys(metadata.custom).length > 0) {
        html += `<div class="metadata-item">
            <strong>Custom Fields:</strong>
            <pre>${JSON.stringify(metadata.custom, null, 2)}</pre>
        </div>`;
    }
    
    html += '</div>';
    
    html += '<h3 style="margin-top: 20px;">Raw Metadata (JSON)</h3>';
    html += `<pre>${JSON.stringify(metadata, null, 2)}</pre>`;
    
    contentDiv.innerHTML = html;
    displayDiv.classList.remove('hidden');
}

function downloadFile() {
    if (!currentFilename) {
        showStatus('No file to download', 'error');
        return;
    }
    
    window.location.href = `/api/download/${currentFilename}`;
    showStatus('Downloading file...', 'info');
}

function showStatus(message, type = 'info') {
    const statusMessages = document.getElementById('statusMessages');
    
    const statusDiv = document.createElement('div');
    statusDiv.className = `status-message ${type}`;
    
    const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
    statusDiv.innerHTML = `<span>${icon}</span><span>${message}</span>`;
    
    statusMessages.appendChild(statusDiv);
    
    setTimeout(() => {
        statusDiv.style.opacity = '0';
        setTimeout(() => {
            statusDiv.remove();
        }, 300);
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function loadAppInfo() {
    fetch('/api/info')
        .then(response => response.json())
        .then(data => {
            console.log('Application Info:', data);
        })
        .catch(error => {
            console.error('Error loading app info:', error);
        });
}
