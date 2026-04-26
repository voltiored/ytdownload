import streamlit as st
import yt_dlp
import tempfile
import os
import re

st.set_page_config(page_title="YT Downloader", page_icon="🎬", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background: #0A0A0A;
    background-image:
        radial-gradient(ellipse at 10% 50%, rgba(255,50,50,0.07) 0%, transparent 55%),
        radial-gradient(ellipse at 90% 20%, rgba(255,50,50,0.05) 0%, transparent 50%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; max-width: 660px !important; }

.hero {
    text-align: center;
    padding: 2.5rem 0 1.8rem;
    animation: fadeUp 0.6s ease both;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,50,50,0.12);
    border: 1px solid rgba(255,50,50,0.3);
    color: #FF5555;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 700;
    color: #F0F0F0;
    line-height: 1.05;
    margin: 0 0 0.5rem;
    letter-spacing: -1.5px;
}
.hero h1 span { color: #FF3333; }
.hero p { font-size: 0.95rem; color: #666; font-weight: 300; margin: 0; }

.sep { border: none; border-top: 1px solid #1E1E1E; margin: 0.5rem 0 1.5rem; }

/* Cookie uploader box */
.cookie-box {
    background: #111;
    border: 1px solid #2A2A2A;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
}
.cookie-box summary {
    color: #666;
    font-size: 0.8rem;
    cursor: pointer;
    letter-spacing: 0.05em;
    font-family: 'Space Mono', monospace;
}
.cookie-box summary:hover { color: #FF5555; }
.cookie-hint {
    color: #444;
    font-size: 0.75rem;
    margin-top: 0.6rem;
    line-height: 1.6;
    font-family: 'Space Mono', monospace;
}
.cookie-hint a { color: #FF5555; text-decoration: none; }

[data-testid="stTextInput"] input {
    background: #111 !important;
    border: 1.5px solid #2A2A2A !important;
    border-radius: 10px !important;
    color: #F0F0F0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #FF3333 !important;
    box-shadow: 0 0 0 3px rgba(255,51,51,0.1) !important;
}
[data-testid="stTextInput"] input::placeholder { color: #444 !important; }
[data-testid="stTextInput"] label {
    color: #888 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
}

[data-testid="stRadio"] label { color: #AAA !important; font-size: 0.85rem !important; }
[data-testid="stSelectbox"] label {
    color: #888 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em !important;
}

/* File uploader para cookies */
[data-testid="stFileUploader"] {
    background: transparent !important;
    border: 1px dashed #2A2A2A !important;
    border-radius: 8px !important;
    padding: 0.5rem !important;
}
[data-testid="stFileUploader"] label { color: #555 !important; font-size: 0.75rem !important; }

div[data-testid="stButton"] { width: 100% !important; }
div[data-testid="stButton"] > button {
    width: 100% !important;
    background: #FF3333 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.85rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s !important;
    margin-top: 0.5rem !important;
}
div[data-testid="stButton"] > button:hover {
    background: #CC0000 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(255,51,51,0.3) !important;
}

div[data-testid="stDownloadButton"] { width: 100% !important; }
div[data-testid="stDownloadButton"] > button {
    width: 100% !important;
    background: #111 !important;
    color: #FF5555 !important;
    border: 1.5px solid #FF3333 !important;
    border-radius: 10px !important;
    padding: 0.85rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    transition: background 0.2s, transform 0.15s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: #1A0A0A !important;
    transform: translateY(-2px) !important;
}

[data-testid="stAlert"] { border-radius: 10px !important; font-size: 0.88rem !important; }

.video-info {
    background: #111;
    border: 1px solid #222;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.75rem 0;
    display: flex;
    gap: 1rem;
    align-items: center;
    animation: fadeUp 0.4s ease both;
}
.video-thumb {
    width: 80px; height: 56px;
    object-fit: cover; border-radius: 6px; flex-shrink: 0;
}
.video-title { color: #F0F0F0; font-size: 0.88rem; font-weight: 500;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 0.2rem; }
.video-dur { color: #555; font-family: 'Space Mono', monospace; font-size: 0.75rem; }

.footer {
    text-align: center; color: #333; font-size: 0.72rem;
    padding: 2rem 0 0.5rem; letter-spacing: 0.06em;
    font-family: 'Space Mono', monospace;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)


# ── HELPERS ──────────────────────────────────────────────────────

def segundos_a_duracion(s):
    s = int(s or 0)
    h, r = divmod(s, 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def opts_base(cookiefile=None):
    o = {
        "quiet": True,
        "no_warnings": True,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        },
    }
    if cookiefile:
        o["cookiefile"] = cookiefile
    return o

def obtener_info(url, cookiefile=None):
    opts = {**opts_base(cookiefile), "skip_download": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)

def descargar_mp3(url, tmpdir, cookiefile=None):
    ruta = os.path.join(tmpdir, "audio.%(ext)s")
    opts = {
        **opts_base(cookiefile),
        "format": "bestaudio/best",
        "outtmpl": ruta,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    return os.path.join(tmpdir, "audio.mp3")

def descargar_mp4(url, tmpdir, calidad, cookiefile=None):
    ruta = os.path.join(tmpdir, "video.%(ext)s")
    fmt = {
        "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "720p":  "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "480p":  "bestvideo[height<=480]+bestaudio/best[height<=480]",
        "360p":  "bestvideo[height<=360]+bestaudio/best[height<=360]",
    }
    opts = {
        **opts_base(cookiefile),
        "format": fmt.get(calidad, "bestvideo+bestaudio/best"),
        "outtmpl": ruta,
        "merge_output_format": "mp4",
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    for f in os.listdir(tmpdir):
        if f.endswith(".mp4"):
            return os.path.join(tmpdir, f)
    raise FileNotFoundError("No se generó el archivo MP4.")

def nombre_seguro(titulo):
    return re.sub(r'[\\/*?:"<>|]', "", titulo)[:60]


# ── INTERFAZ ─────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <div class="hero-badge">⬇ USO PERSONAL</div>
    <h1>YT<span>Down</span></h1>
    <p>Descarga vídeos y audio de YouTube sin complicaciones.</p>
</div>
<hr class="sep">
""", unsafe_allow_html=True)

# ── Sección cookies (desplegable) ────────────────────────────────
with st.expander("🍪 ¿La app no carga el vídeo? Sube tus cookies de YouTube"):
    st.markdown("""
**¿Por qué?** Streamlit Cloud usa servidores en la nube que YouTube bloquea. Las cookies de tu sesión de YouTube hacen que la petición parezca tuya.

**Cómo obtener el archivo `cookies.txt`:**
1. Instala la extensión **"Get cookies.txt LOCALLY"** en Chrome o Firefox
2. Ve a [youtube.com](https://youtube.com) con tu cuenta iniciada
3. Haz clic en la extensión → **"Export cookies"** → guarda el archivo
4. Súbelo aquí abajo ↓
""")
    cookie_file = st.file_uploader("Sube cookies.txt", type=["txt"], label_visibility="collapsed")

# Guardar cookies en fichero temporal si se subieron
cookiepath = None
if cookie_file:
    tmp_cookie = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="wb")
    tmp_cookie.write(cookie_file.read())
    tmp_cookie.flush()
    cookiepath = tmp_cookie.name
    st.success("🍪 Cookies cargadas correctamente")

# ── URL y opciones ───────────────────────────────────────────────
url = st.text_input("URL DEL VÍDEO", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns([1, 1])
with col1:
    formato = st.radio("FORMATO", ["🎵 MP3", "🎬 MP4"], horizontal=True)
with col2:
    calidad = st.selectbox(
        "CALIDAD (solo MP4)",
        ["1080p", "720p", "480p", "360p"],
        disabled=(formato == "🎵 MP3")
    )

# ── Preview ──────────────────────────────────────────────────────
info = None
if url and ("youtube.com" in url or "youtu.be" in url):
    with st.spinner("Obteniendo información..."):
        try:
            info = obtener_info(url, cookiepath)
            thumb = info.get("thumbnail", "")
            titulo = info.get("title", "Sin título")
            duracion = segundos_a_duracion(info.get("duration", 0))
            st.markdown(f"""
            <div class="video-info">
                <img class="video-thumb" src="{thumb}" onerror="this.style.display='none'">
                <div class="video-meta">
                    <div class="video-title">{titulo}</div>
                    <div class="video-dur">⏱ {duracion}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"No se pudo obtener la información del vídeo. {'Prueba a subir tus cookies 🍪' if not cookiepath else str(e)}")

# ── Descarga ─────────────────────────────────────────────────────
if st.button("⬇ Descargar"):
    if not url:
        st.error("Introduce una URL primero.")
    elif not info:
        st.error("URL no válida o vídeo no disponible.")
    else:
        nombre = nombre_seguro(info.get("title", "video"))
        tmpdir = tempfile.mkdtemp()

        with st.spinner("Descargando... esto puede tardar unos segundos ⏳"):
            try:
                if formato == "🎵 MP3":
                    ruta = descargar_mp3(url, tmpdir, cookiepath)
                    with open(ruta, "rb") as f:
                        st.success("✅ Audio listo")
                        st.download_button("⬇ Descargar MP3", f,
                            file_name=f"{nombre}.mp3", mime="audio/mpeg")
                else:
                    ruta = descargar_mp4(url, tmpdir, calidad, cookiepath)
                    with open(ruta, "rb") as f:
                        st.success(f"✅ Vídeo listo ({calidad})")
                        st.download_button("⬇ Descargar MP4", f,
                            file_name=f"{nombre}.mp4", mime="video/mp4")
            except Exception as e:
                st.error(f"❌ Error al descargar: {e}")

st.markdown("""
<div class="footer">
    YTDOWN · SOLO USO PERSONAL · HECHO CON PYTHON + STREAMLIT
</div>
""", unsafe_allow_html=True)
