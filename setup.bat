@echo off
REM Script de instalación rápida para TranscriptorIA (Windows)

echo.
echo 🚀 Instalación rápida de TranscriptorIA
echo =========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado
    pause
    exit /b 1
)

echo ✓ Python encontrado:
python --version

REM Verificar FFmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  FFmpeg no está instalado
    echo    Descárgalo desde: https://ffmpeg.org/download.html
    echo    Y agrégalo al PATH
    pause
    exit /b 1
)

echo ✓ FFmpeg encontrado
echo.

REM Crear virtual env
echo 📦 Creando virtual environment...
python -m venv venv

REM Activar venv
call venv\Scripts\activate.bat

echo ✓ Virtual environment activado
echo.

REM Instalar dependencias
echo 📥 Instalando dependencias...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
pip install flask-cors >nul 2>&1

echo ✓ Dependencias instaladas
echo.

REM Crear directorios
echo 📁 Creando directorios...
if not exist "audios\uploads" mkdir audios\uploads
if not exist "salidas" mkdir salidas
if not exist "modelos" mkdir modelos

echo ✓ Directorios creados
echo.

echo =========================================
echo ✅ ¡Instalación completada!
echo.
echo 📝 Para iniciar el servidor:
echo    cd src
echo    python app_cors.py
echo.
echo 🌐 Luego abre: http://localhost:5000
echo    O si usas GitHub Pages: docs\index.html
echo.
echo 📖 Documentación: ver README.md
echo =========================================
echo.
pause
