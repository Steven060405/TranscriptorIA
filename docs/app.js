// Configuración
let apiUrl = localStorage.getItem('apiUrl') || 'http://localhost:5000';
let currentJobId = null;
let statusCheckInterval = null;

// Cargar URL guardada
document.getElementById('apiUrl').value = apiUrl;

// Event Listeners
document.getElementById('apiUrl').addEventListener('change', (e) => {
    apiUrl = e.target.value;
    localStorage.setItem('apiUrl', apiUrl);
});

document.getElementById('uploadForm').addEventListener('submit', handleUpload);

// Manejar carga de archivos
async function handleUpload(e) {
    e.preventDefault();
    
    const files = document.getElementById('audioFiles').files;
    if (files.length === 0) {
        showError('Selecciona al menos un archivo de audio');
        return;
    }
    
    const formData = new FormData();
    for (let file of files) {
        formData.append('files', file);
    }
    
    try {
        // Limpiar errores previos
        clearError();
        
        // Mostrar progreso
        document.getElementById('progressContainer').style.display = 'block';
        document.getElementById('resultContainer').style.display = 'none';
        document.getElementById('errorContainer').style.display = 'none';
        document.getElementById('submitBtn').disabled = true;
        
        // Subir archivos
        const uploadResponse = await fetch(`${apiUrl}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const uploadData = await uploadResponse.json();
        
        if (!uploadResponse.ok) {
            throw new Error(uploadData.error || 'Error al subir');
        }
        
        currentJobId = uploadData.job_id;
        if (!currentJobId) {
            throw new Error('No se recibió ID de trabajo');
        }
        
        startStatusCheck();
        
    } catch (error) {
        showError(`Error al subir: ${error.message}`);
        document.getElementById('progressContainer').style.display = 'none';
        document.getElementById('submitBtn').disabled = false;
    }
}

// Iniciar verificación de estado
function startStatusCheck() {
    if (statusCheckInterval) clearInterval(statusCheckInterval);
    
    // Verificar inmediatamente
    checkStatus();
    
    // Luego cada 2 segundos
    statusCheckInterval = setInterval(checkStatus, 2000);
}

// Verificar estado del trabajo
async function checkStatus() {
    try {
        const response = await fetch(`${apiUrl}/job-status/${currentJobId}`, {
            headers: { 'Accept': 'application/json' }
        });
        
        if (!response.ok) throw new Error('Failed to fetch status');
        
        const job = await response.json();
        
        // Actualizar UI según estado
        const statusText = document.getElementById('statusText');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        
        const statusMap = {
            'queued': 'En cola...',
            'splitting': 'Dividiendo audio...',
            'transcribing': 'Transcribiendo...',
            'done': 'Completado',
            'error': 'Error'
        };
        
        statusText.textContent = statusMap[job.status] || job.status;
        
        if (job.total > 0) {
            const percentage = Math.round((job.progress / job.total) * 100);
            progressBar.style.width = percentage + '%';
            progressText.textContent = `${job.progress} / ${job.total} chunks`;
        }
        
        // Si está listo o hay error
        if (job.status === 'done') {
            clearInterval(statusCheckInterval);
            showResults(job);
        } else if (job.status === 'error') {
            clearInterval(statusCheckInterval);
            showError(job.error || 'Error desconocido');
            document.getElementById('progressContainer').style.display = 'none';
            document.getElementById('submitBtn').disabled = false;
        }
        
    } catch (error) {
        console.error('Error checking status:', error);
    }
}

// Mostrar resultados
function showResults(job) {
    document.getElementById('progressContainer').style.display = 'none';
    document.getElementById('resultContainer').style.display = 'block';
    document.getElementById('submitBtn').disabled = false;
    
    // Mostrar transcripción
    const resultText = document.getElementById('resultText');
    resultText.innerHTML = '';
    
    if (job.result && job.result.length > 0) {
        job.result.forEach(item => {
            const div = document.createElement('div');
            div.className = 'list-group-item';
            div.innerHTML = `
                <div class="speaker-tag">${escapeHtml(item.role || item.speaker)}</div>
                <div class="trans-text">${escapeHtml(item.text)}</div>
            `;
            resultText.appendChild(div);
        });
    }
    
    // Configurar descargas
    if (job.txt_name) {
        document.getElementById('downloadTxt').href = `${apiUrl}/salidas/${job.txt_name}`;
        document.getElementById('downloadTxt').style.display = 'inline-block';
    }
    
    if (job.docx_names && job.docx_names.length > 0) {
        document.getElementById('downloadDocx').href = `${apiUrl}/salidas/${job.docx_names[0]}`;
        document.getElementById('downloadDocx').style.display = 'inline-block';
    }
    
    // Limpiar formulario
    document.getElementById('uploadForm').reset();
}

// Mostrar error
function showError(message) {
    const errorAlert = document.getElementById('errorAlert');
    errorAlert.innerHTML = `<div class="alert alert-danger">${escapeHtml(message)}</div>`;
    
    const errorContainer = document.getElementById('errorContainer');
    document.getElementById('errorText').textContent = message;
    errorContainer.style.display = 'block';
}

// Limpiar error
function clearError() {
    document.getElementById('errorAlert').innerHTML = '';
    document.getElementById('errorContainer').style.display = 'none';
}

// Escapar HTML
function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

