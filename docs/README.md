# TranscriptorIA - GitHub Pages

Esta es la versión web de TranscriptorIA adaptada para funcionar con GitHub Pages.

## 🚀 Cómo usar

### Opción 1: GitHub Pages + Servidor Local

1. **Habilita GitHub Pages** en tu repositorio:
   - Ve a Settings → Pages
   - Selecciona "Deploy from a branch"
   - Elige "main" branch y carpeta "/docs"
   - Guarda

2. **Inicia el servidor localmente**:
   ```bash
   cd src
   pip install flask-cors  # Si no lo tienes
   python app_cors.py
   ```

3. **Accede a GitHub Pages**:
   - URL: `https://tu-usuario.github.io/TranscriptorIA`
   - En "URL del servidor API" escribe: `http://localhost:5000`

### Opción 2: GitHub Pages + Servidor en la nube

1. **Despliega el backend** en un servicio como:
   - [Render.com](https://render.com) (gratis con limitaciones)
   - [Heroku](https://www.heroku.com)
   - [Replit](https://replit.com)
   - Tu propio servidor

2. **Archivo de configuración para Render** (`render.yaml`):
   ```yaml
   services:
   - type: web
     name: transcriptor-api
     runtime: python310
     buildCommand: "pip install -r requirements.txt && pip install flask-cors"
     startCommand: "cd src && python app_cors.py"
     envVars:
     - key: FLASK_ENV
       value: production
   ```

3. **Usa la URL de tu servidor**:
   - En la interfaz de GitHub Pages, escribe la URL de tu servidor en la nube

### Opción 3: Todo en GitHub Pages (Requisito especial)

Para servir todo desde GitHub Pages (incluyendo el backend) necesitarías usar:
- GitHub Actions para procesamiento
- Un servicio de storage para archivos
- Web Workers / Service Workers para procesamiento en cliente

Esto requiere cambios arquitectónicos mayores. Contacta si necesitas esta opción.

## 📋 Requisitos del Servidor

El servidor debe tener:
- Python 3.8+
- FFmpeg instalado y en PATH
- Modelos de whisperx descargados o acceso a internet
- Suficiente RAM y GPU (recomendado)

### Instalación de dependencias:

```bash
# En Windows
pip install -r requirements.txt
pip install flask-cors

# En Linux/Mac
pip3 install -r requirements.txt
pip3 install flask-cors
```

## 🔧 Configuración

### Variables de entorno

```bash
# Puerto (default: 5000)
export FLASK_PORT=5000

# Debug mode (default: false)
export FLASK_DEBUG=true

# Ruta de uploads (default: audios/uploads)
export UPLOAD_DIR=/custom/path
```

### CORS

La API tiene CORS habilitado para:
- `/upload` - Subir archivos
- `/job-status/*` - Ver estado de procesos
- `/salidas/*` - Descargar resultados

Para cambiar las políticas CORS, edita `src/app_cors.py`:

```python
CORS(app, resources={
    r"/upload": {"origins": ["https://tu-dominio.com"]},
    # ...
})
```

## 📱 Uso

1. **Configura la URL del servidor**
   - Puede ser `http://localhost:5000` (local)
   - O la URL de tu servidor en la nube

2. **Prueba la conexión**
   - Haz clic en "Probar conexión"
   - Deberías ver ✓ Conexión exitosa

3. **Sube audios**
   - Selecciona uno o más archivos de audio
   - Haz clic en "Subir y transcribir"

4. **Espera a que se procese**
   - Verás el progreso en tiempo real
   - Los chunks se eliminarán automáticamente al terminar

5. **Descarga resultados**
   - Descarga como TXT o DOCX
   - Los archivos se guardan en `salidas/`

## 🐛 Solución de problemas

### "No se puede conectar al servidor"
- Verifica que el servidor esté corriendo
- Revisa que la URL sea correcta
- En desarrollo local, usa `http://localhost:5000` (sin https)
- Si está en la nube, asegúrate que el URL sea público

### "Error de CORS"
- Asegúrate de usar `app_cors.py` en lugar de `app.py`
- Los orígenes CORS están configurados en `app_cors.py`

### "FFmpeg no encontrado"
- En Windows: Descarga desde https://ffmpeg.org/download.html
- En Linux: `sudo apt-get install ffmpeg`
- En Mac: `brew install ffmpeg`

### Archivos no se limpian
- Si ves archivos en `audios/uploads`, revisa los logs del servidor
- El script intenta limpiar automáticamente

## 📝 Cambios en esta versión

### Para GitHub Pages:
- ✅ Interfaz completamente estática en `/docs`
- ✅ Configuración de servidor dinámica
- ✅ CORS habilitado en el API

### Para eliminar chunks:
- ✅ Se eliminan automáticamente después de transcribir
- ✅ También se eliminan si hay error
- ✅ Se elimina el archivo de audio original también

## 🔐 Seguridad

⚠️ **Notas importantes**:

1. **En producción**, usa HTTPS
2. **Valida archivos** - verifica tipos MIME antes de procesar
3. **Rate limiting** - considera agregar límites de requests
4. **Autenticación** - considera agregar token/contraseña
5. **Limpieza** - los archivos se limpian en 5-10 minutos

Ejemplo con autenticación:

```python
@app.route("/upload", methods=["POST"])
def upload():
    token = request.headers.get('Authorization')
    if token != 'Bearer TU_TOKEN_SECRETO':
        return jsonify({"error": "Unauthorized"}), 401
    # ... resto del código
```

## 📞 Soporte

Para reportar problemas o sugerencias, crea un issue en el repositorio.

---

**Made with ❤️ para transcribir audios con IA**
