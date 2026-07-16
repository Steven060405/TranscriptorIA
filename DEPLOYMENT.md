# Guía de Deployment

## 🚀 Deploy rápido en Render.com

### Paso 1: Preparar repositorio

1. Asegúrate de tener en tu repositorio:
   - `render.yaml`
   - `requirements.txt` con `flask-cors`
   - Directorio `docs/` con interfaz

2. Si no tienes `flask-cors` en requirements.txt, agrégalo:
   ```bash
   echo "flask-cors>=4.0" >> requirements.txt
   ```

### Paso 2: Conectar con Render

1. Ve a [render.com](https://render.com)
2. Haz login con GitHub
3. Ve a "Dashboard" → "New +" → "Web Service"
4. Selecciona tu repositorio de TranscriptorIA
5. Render detectará el `render.yaml` automáticamente
6. Haz clic en "Deploy"

### Paso 3: Usar GitHub Pages + Render

1. **URL de GitHub Pages**: `https://tu-usuario.github.io/TranscriptorIA/`
2. **En la interfaz**, usa como "URL del servidor API":
   ```
   https://transcriptor-api.onrender.com
   ```
   (reemplaza con tu URL de Render)

## 📦 Deploy en Heroku (Legacy)

Heroku ahora es de pago. Usa Render en su lugar.

## 🐳 Deploy con Docker

Si tienes Docker instalado:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copiar archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir flask-cors

COPY src/ ./src

WORKDIR /app/src

# Crear directorios
RUN mkdir -p ../audios/uploads ../salidas

CMD ["python", "app_cors.py"]
```

Luego:
```bash
docker build -t transcriptor-ia .
docker run -p 5000:5000 -v $(pwd)/audios:/app/audios transcriptor-ia
```

## 🌐 Deploy en tu propio servidor VPS

### En Ubuntu/Debian:

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3 python3-pip ffmpeg

# Clonar repositorio
git clone https://github.com/tu-usuario/TranscriptorIA.git
cd TranscriptorIA

# Crear virtual env
python3 -m venv venv
source venv/bin/activate

# Instalar paquetes
pip install -r requirements.txt
pip install flask-cors gunicorn

# Ejecutar con Gunicorn
cd src
gunicorn -w 4 -b 0.0.0.0:5000 app_cors:app
```

### Configurar con systemd (para que inicie automáticamente):

```bash
sudo nano /etc/systemd/system/transcriptor.service
```

```ini
[Unit]
Description=TranscriptorIA
After=network.target

[Service]
Type=notify
WorkingDirectory=/home/tu-usuario/TranscriptorIA/src
ExecStart=/home/tu-usuario/TranscriptorIA/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app_cors:app
Restart=always
User=tu-usuario

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable transcriptor
sudo systemctl start transcriptor
```

## 🔒 Configurar Nginx como proxy inverso

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'Content-Type';
    }
}
```

## 📊 Monitorar recursos

En producción, monitorea:

```bash
# Ver uso de CPU/RAM
top

# Ver logs del servicio
sudo journalctl -u transcriptor -f

# Ver espacio en disco
df -h
```

## 🆘 Troubleshooting

### "Error: ffmpeg not found"
```bash
# Instalar ffmpeg
sudo apt install ffmpeg  # Linux
brew install ffmpeg      # Mac
# En Windows, descarga desde ffmpeg.org
```

### "Port 5000 already in use"
```bash
# Cambiar puerto en app_cors.py, o:
lsof -i :5000  # Identificar proceso
kill -9 PID    # Matar proceso (si es seguro)
```

### "Timeout on large files"
- Aumenta timeout en Render settings
- Reduce tamaño de chunks en `splitter.py`

---

¿Necesitas ayuda? Crea un issue en el repositorio.
