#!/bin/bash
# Script de instalación rápida para TranscriptorIA
# Ejecutar: bash setup.sh

echo "🚀 Instalación rápida de TranscriptorIA"
echo "========================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

echo "✓ Python encontrado: $(python3 --version)"

# Verificar FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg no está instalado"
    echo "   Instálalo antes de continuar:"
    echo "   - Windows: descarga desde ffmpeg.org"
    echo "   - Linux: sudo apt install ffmpeg"
    echo "   - Mac: brew install ffmpeg"
    exit 1
fi

echo "✓ FFmpeg encontrado: $(ffmpeg -version | head -n1)"
echo ""

# Crear virtual env
echo "📦 Creando virtual environment..."
python3 -m venv venv

# Activar venv
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    source venv/Scripts/activate  # Para Windows Git Bash
fi

echo "✓ Virtual environment activado"
echo ""

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
pip install flask-cors > /dev/null 2>&1

echo "✓ Dependencias instaladas"
echo ""

# Crear directorios
echo "📁 Creando directorios..."
mkdir -p audios/uploads
mkdir -p salidas
mkdir -p modelos

echo "✓ Directorios creados"
echo ""

echo "========================================="
echo "✅ ¡Instalación completada!"
echo ""
echo "📝 Para iniciar el servidor:"
echo "   source venv/bin/activate"
echo "   cd src"
echo "   python app_cors.py"
echo ""
echo "🌐 Luego abre: http://localhost:5000"
echo "   O si usas GitHub Pages: docs/index.html"
echo ""
echo "📖 Documentación: ver README.md"
echo "========================================="
