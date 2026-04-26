# 🎬 YTDown

Descargador de vídeos de YouTube en MP3 y MP4, hecho con Python + Streamlit.

> ⚠️ Solo para uso personal y aprendizaje.

## Funcionalidades

- Previsualización del vídeo (título, miniatura, duración) antes de descargar
- Descarga en **MP3** (192 kbps)
- Descarga en **MP4** con selección de calidad: 1080p / 720p / 480p / 360p
- Nombre del archivo = título del vídeo

## Ejecutar en local

```bash
# Instalar dependencias del sistema
# Ubuntu/Debian:
sudo apt install ffmpeg
# macOS:
brew install ffmpeg

# Instalar dependencias Python
pip install -r requirements.txt

# Arrancar la app
streamlit run app.py
```

## Estructura

```
ytdl/
├── app.py            # App principal
├── requirements.txt  # Dependencias Python (streamlit, yt-dlp)
├── packages.txt      # Dependencias sistema (ffmpeg)
└── README.md
```

## Tecnologías que aprenderás aquí

- **Streamlit** — interfaces web rápidas en Python
- **yt-dlp** — descarga de vídeos (fork mejorado de youtube-dl)
- **ffmpeg** — conversión y mezcla de audio/vídeo
- **tempfile** — gestión de archivos temporales
- **subprocess / postprocessors** — llamadas a herramientas externas desde Python
