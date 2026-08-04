from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import json
import os
import shutil

app = FastAPI(title="Panel Bots VIP")

CONFIG_FILE = "config.json"
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "grupo_publico": "",
            "grupo_vip": "",
            "precio_vip": "20",
            "qr_yape": "",
            "admins": [],
            "bots": []
        }, f, indent=4)


def cargar_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


app.mount(
    "/static",
    StaticFiles(directory="."),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
async def inicio():

    config = cargar_config()

    return f"""
    <html>
    <head>
        <title>Panel Bots VIP</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>

    <body>

    <div class="panel">

    <h1>🤖 Panel Bots VIP</h1>

    <form method="post">

    <h3>🔗 Grupo Público</h3>
    <input name="grupo_publico"
    value="{config.get('grupo_publico','')}">

    <h3>💎 Grupo VIP</h3>
    <input name="grupo_vip"
    value="{config.get('grupo_vip','')}">

    <h3>💰 Precio VIP</h3>
    <input name="precio"
    value="{config.get('precio_vip','20')}">

    <h3>🤖 Token Bot</h3>
    <input name="token"
    placeholder="Token del bot">

    <br><br>

    <button>
    💾 Guardar
    </button>

    </form>


    <h3>📷 QR Yape</h3>

    <form action="/subir-qr"
    method="post"
    enctype="multipart/form-data">

    <input type="file" name="qr">

    <button>
    📤 Subir QR
    </button>

    </form>


    </div>

    </body>
    </html>
    """


@app.post("/")
async def guardar(
    grupo_publico: str = Form(""),
    grupo_vip: str = Form(""),
    precio: str = Form(""),
    token: str = Form("")
):

    config = cargar_config()

    config["grupo_publico"] = grupo_publico
    config["grupo_vip"] = grupo_vip
    config["precio_vip"] = precio


    if token:
        config["bots"].append({
            "token": token,
            "activo": True
        })


    guardar_config(config)

    return RedirectResponse(
        "/",
        status_code=303
    )


@app.post("/subir-qr")
async def subir_qr(
    qr: UploadFile = File(...)
):

    ruta = "uploads/qr_yape.png"

    with open(ruta, "wb") as buffer:
        shutil.copyfileobj(
            qr.file,
            buffer
        )


    config = cargar_config()

    config["qr_yape"] = ruta

    guardar_config(config)


    return RedirectResponse(
        "/",
        status_code=303
    )


# =========================
# INICIAR PANEL WEB
# =========================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
