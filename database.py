# database.py

import sqlite3
from datetime import datetime


DB = "usuarios.db"



def conectar():
    return sqlite3.connect(DB)



# ==========================
# CREAR TABLAS
# ==========================

def crear_tablas():

    conn = conectar()
    cursor = conn.cursor()


    # Usuarios

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (

        id INTEGER PRIMARY KEY,
        username TEXT,
        vip INTEGER DEFAULT 0,
        fecha TEXT

    )
    """)



    # Pagos

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





# ==========================
# REGISTRAR USUARIO
# ==========================

def registrar_usuario(
    user_id,
    username
):

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
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )
        )
    )


    conn.commit()
    conn.close()





# ==========================
# OBTENER USUARIOS
# ==========================

def obtener_usuarios():

    conn = conectar()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT id, username, vip
        FROM usuarios
        """
    )


    datos = cursor.fetchall()

    conn.close()


    lista = []


    for usuario in datos:

        lista.append(
            {
                "id": usuario[0],
                "username": usuario[1],
                "vip": usuario[2]
            }
        )


    return lista





# ==========================
# ACTIVAR VIP
# ==========================

def activar_vip(
    user_id
):

    conn = conectar()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE usuarios

        SET vip = 1

        WHERE id = ?
        """,
        (
            user_id,
        )
    )


    conn.commit()
    conn.close()





# ==========================
# GUARDAR PAGO
# ==========================

def guardar_pago(
    user_id,
    comprobante
):

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
            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )
        )
    )


    conn.commit()
    conn.close()





# ==========================
# PAGOS PENDIENTES
# ==========================

def obtener_pago(
    pago_id
):

    conn = conectar()
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM pagos

        WHERE id = ?

        """,
        (
            pago_id,
        )
    )


    pago = cursor.fetchone()


    conn.close()


    return pago





# ==========================
# CAMBIAR ESTADO PAGO
# ==========================

def actualizar_pago(
    pago_id,
    estado
):

    conn = conectar()
    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE pagos

        SET estado = ?

        WHERE id = ?

        """,
        (
            estado,
            pago_id
        )
    )


    conn.commit()
    conn.close()





# Crear base al iniciar

crear_tablas()
