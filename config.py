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


# Archivo configuración
CONFIG_FILE = "config.json"


# Token principal opcional
BOT_TOKEN = os.getenv(
    "BOT_TOKEN",
    ""
)


# Base de datos
DATABASE = "usuarios.db"


# Grupo público
GRUPO_PUBLICO = "https://t.me/+MIGBEvQEdyZlNzgx"


# Grupo VIP
GRUPO_VIP = "https://t.me/+TDY6tCd4J1lkZjUx"


# Precio mostrado
PRECIO = "S/20"


# Ruta del QR Yape
QR_YAPE = "uploads/qr_yape.png"
