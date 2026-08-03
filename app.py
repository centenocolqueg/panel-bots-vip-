from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import json
import os

app = FastAPI(title="Panel Bots VIP")

CONFIG_FILE = "config.json"

# Crear configuración inicial
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "grupo_publico": "",
            "grupo_vip": "",
            "precio_vip": "20",
            "qr_yape": "",
            "admins": [
                8315143020,
                8616315480
            ],
            "bots": []
        }, f, indent=4)


def cargar_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


app.mount("/static", StaticFiles(directory="."), name="static")


@app.get("/", response_class=HTMLResponse)
async def inicio():
    config = cargar_config()

    html = """
    <html>
    <head>
        <title>Panel Bots VIP</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>

    <body>

    <h1>🤖 Panel Bots VIP</h1>

    <form method="post">

    <h3>🔗 Grupo Público</h3>
    <input name="grupo_publico" value="{publico}">

    <h3>💎 Grupo VIP</h3>
    <input name="grupo_vip" value="{vip}">

    <h3>💰 Precio VIP</h3>
    <input name="precio" value="{precio}">

    <h3>🤖 Token Bot</h3>
    <input name="token" placeholder="Token del bot">

    <br><br>
    <button>💾 Guardar</button>

    </form>

    </body>
    </html>
    """.format(
        publico=config["grupo_publico"],
        vip=config["grupo_vip"],
        precio=config["precio_vip"]
    )

    return html


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

    return RedirectResponse("/", status_code=303)
