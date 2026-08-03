# config.py

import os
from dotenv import load_dotenv

load_dotenv()


# Nombre del sistema
NOMBRE = "Panel Bots VIP"


# Precio VIP
PRECIO_VIP = 20


# Administradores Telegram
ADMINS = [
    8315143020,
    8616315480
]


# Archivo donde se guarda la configuración
CONFIG_FILE = "config.json"


# Token opcional del bot principal
BOT_TOKEN = os.getenv(
    "BOT_TOKEN",
    ""
)


# Base de datos
DATABASE = "usuarios.db"


# Enlaces iniciales
GRUPO_PUBLICO = "https://t.me/+MIGBEvQEdyZlNzgx"

GRUPO_VIP = "https://t.me/+TDY6tCd4J1lkZjUx"


# QR Yape
QR_YAPE = ""
