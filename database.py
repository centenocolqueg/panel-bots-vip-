# database.py

import sqlite3
from datetime import datetime


DB = "usuarios.db"


def conectar():
    return sqlite3.connect(DB)


# Crear tablas
def crear_tablas():

    conn = conectar()
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (

        id INTEGER PRIMARY KEY,
        username TEXT,
        vip INTEGER DEFAULT 0,
        fecha TEXT

    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pagos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        comprobante TEXT,
        estado TEXT DEFAULT 'pendiente',
        fecha TEXT

    )
    """)


    conn.commit()
    conn.close()



# Registrar usuario nuevo
def registrar_usuario(user_id, username):

    conn = conectar()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT OR IGNORE INTO usuarios
        (id, username, fecha)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            username,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
    )


    conn.commit()
    conn.close()



# Obtener todos los usuarios
def obtener_usuarios():

    conn = conectar()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT id, username, vip FROM usuarios"
    )


    datos = cursor.fetchall()

    conn.close()


    usuarios = []

    for u in datos:
        usuarios.append(
            {
                "id": u[0],
                "username": u[1],
                "vip": u[2]
            }
        )


    return usuarios



# Activar VIP
def activar_vip(user_id):

    conn = conectar()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE usuarios
        SET vip = 1
        WHERE id = ?
        """,
        (user_id,)
    )


    conn.commit()
    conn.close()



# Crear solicitud de pago
def guardar_pago(user_id, comprobante):

    conn = conectar()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO pagos
        (usuario_id, comprobante, fecha)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            comprobante,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
    )


    conn.commit()
    conn.close()



crear_tablas()
