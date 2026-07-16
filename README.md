# 🚀 TranscriptorIA - GitHub Pages & API

Herramienta web para transcribir audios largos usando IA (WhisperX) con diarización automática.

## ⚡ Inicio rápido

### Para usuarios (usar la app web):

1. **Inicia el servidor** (ver abajo "Instalación")
2. **Abre GitHub Pages**:
   - Si está deployado: `https://tu-usuario.github.io/TranscriptorIA`
   - Si es local: Abre `docs/index.html` en tu navegador
3. **Configura el servidor**:
   - URL local: `http://localhost:5000`
   - URL remota: Tu URL de deploy en Render/Heroku/etc
4. **Prueba la conexión** ✓
5. **Sube tus audios** y espera

### Para desarrolladores:

```bash
# Clonar y setup
git clone https://github.com/tu-usuario/TranscriptorIA.git
cd TranscriptorIA

# Crear venv
python -m venv venv
source venv/bin/activate  # o: venv\Scripts\activate en Windows

# Instalar dependencias
pip install -r requirements.txt
pip install flask-cors

# Ejecutar
cd src
python app_cors.py
```

## 📋 Archivos importantes

| Archivo | Descripción |
|---------|-------------|
| `docs/` | Interfaz web estática para GitHub Pages |
| `src/app_cors.py` | Backend API con CORS habilitado |
| `src/app.py` | Backend original (usa para GUI local) |
| `DEPLOYMENT.md` | Guía completa de deployment |
| `render.yaml` | Configuración para Render.com |

## 🔄 Flujo de trabajo

```
Cliente (GitHub Pages)
    ↓ sube archivos
    ↓
API Server (app_cors.py)
    ↓ divide en chunks + transcribe
    ↓
Genera TXT/DOCX
    ↓ **elimina chunks automáticamente**
    ↓
Cliente descarga resultados
```

## ✨ Características nuevas

✅ **Interfaz en GitHub Pages** - Accesible desde cualquier navegador  
✅ **CORS habilitado** - Funciona con backends remotos  
✅ **Limpieza automática** - Chunks se eliminan al terminar  
✅ **Configuración dinámica** - Cambia URL del servidor sin compilar  
✅ **Soporte multi-archivo** - Procesa varios audios a la vez  

## 🌍 Deployment opciones

| Opción | Costo | Configuración | Notas |
|--------|-------|---------------|-------|
| **Local** | Gratis | 5 min | Para desarrollo |
| **Render** | Gratis* | 10 min | Recomendado (*limita después de 15 min inactividad) |
| **Replit** | Gratis* | 10 min | Fácil, pero lento |
| **VPS propio** | $5-20/mes | 30 min | Máximo control |

👉 **Ver [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones detalladas**

## 🆘 Problemas comunes

**"No se conecta al servidor"**
- ¿El servidor está corriendo?
- ¿La URL es correcta? (sin slash al final)
- ¿Está en desarrollo? Usa `http://localhost:5000`

**"Error de CORS"**
- Usa `app_cors.py`, no `app.py`
- El CORS ya está configurado para `*`

**"FFmpeg no encontrado"**
- Windows: Descarga [ffmpeg.org](https://ffmpeg.org/download.html)
- Linux: `sudo apt install ffmpeg`
- Mac: `brew install ffmpeg`

**"Archivos no se limpian"**
- Se limpian automáticamente en `audios/uploads/chunks_*`
- Si no se limpian, revisa permisos en la carpeta

## 📱 Cómo GitHub Pages + Backend API funciona

```
GitHub Pages      Backend API (Render/Local)
┌────────────────┐      ┌──────────────────┐
│ index.html     │ POST │ /upload          │
│ app.js         │─────→│                  │
│ style.css      │ GET  │ /job-status      │
└────────────────┘←─────│                  │
                   GET  │ /salidas         │
                  ←─────┘                  │
                        └──────────────────┘
```

## 🔧 Configuración

### Variables de entorno:
```bash
export FLASK_ENV=production
export FLASK_DEBUG=false
export FLASK_PORT=5000
```

### Personalizar CORS:
```python
# src/app_cors.py
CORS(app, resources={
    r"/upload": {"origins": ["https://mi-sitio.com"]},
})
```

## 📦 Requisitos de sistema

- Python 3.8+
- FFmpeg
- 4GB RAM mínimo (8GB recomendado)
- GPU NVIDIA (opcional pero recomendado)

### Instalar FFmpeg:

**Windows:**
- Descarga desde https://ffmpeg.org/download.html
- O: `choco install ffmpeg`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

## 📞 Support

- 📖 Documentación: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🐛 Reportar bugs: Issues en GitHub
- 💡 Sugerencias: Discussions en GitHub

## 📄 Licencia

MIT License - Usa libremente en tus proyectos

---

**Made with ❤️ para transcribir audios con IA**

*TranscriptorIA usa WhisperX para transcripción y PyDiarize para diarización automática*
