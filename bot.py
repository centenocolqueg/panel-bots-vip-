# bot.py

import asyncio
import json
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database import (
    registrar_usuario,
    obtener_usuarios
)


CONFIG_FILE = "config.json"


def cargar_config():

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)



def menu_usuario():

    config = cargar_config()

    botones = []

    if config.get("grupo_publico"):

        botones.append(
            [
                InlineKeyboardButton(
                    text="📢 Grupo Público",
                    url=config["grupo_publico"]
                )
            ]
        )


    botones.append(
        [
            InlineKeyboardButton(
                text="💎 Comprar VIP S/20",
                callback_data="comprar_vip"
            )
        ]
    )


    botones.append(
        [
            InlineKeyboardButton(
                text="👤 Mi Cuenta",
                callback_data="cuenta"
            )
        ]
    )


    return InlineKeyboardMarkup(
        inline_keyboard=botones
    )



def crear_bot(token):

    bot = Bot(
        token=token
    )

    dp = Dispatcher()



    # ==========================
    # INICIO USUARIO
    # ==========================

    @dp.message(Command("start"))
    async def start(message: types.Message):

        registrar_usuario(
            message.from_user.id,
            message.from_user.username
        )


        await message.answer(
            "🤖 Bienvenido\n\n"
            "Selecciona una opción:",
            reply_markup=menu_usuario()
        )



    # ==========================
    # COMPRA VIP
    # ==========================

    @dp.callback_query(
        F.data == "comprar_vip"
    )
    async def comprar_vip(
        call: types.CallbackQuery
    ):

        config = cargar_config()


        await call.message.answer(
            "💎 Compra VIP\n\n"
            f"Precio: S/ {config.get('precio_vip','20')}\n\n"
            "Realiza el pago por Yape.\n"
            "Luego envía tu comprobante."
        )


        qr = config.get(
            "qr_yape",
            ""
        )


        if qr and os.path.exists(qr):

            await call.message.answer_photo(
                photo=open(qr, "rb"),
                caption="📷 QR de Yape"
            )



    # ==========================
    # MI CUENTA
    # ==========================

    @dp.callback_query(
        F.data == "cuenta"
    )
    async def cuenta(
        call: types.CallbackQuery
    ):

        await call.message.answer(
            "👤 Mi cuenta\n\n"
            f"ID: {call.from_user.id}"
        )



    # ==========================
    # ANUNCIO ADMIN
    # ==========================

    @dp.message(Command("anuncio"))
    async def anuncio(
        message: types.Message
    ):

        config = cargar_config()


        if message.from_user.id not in config["admins"]:
            return



        texto = message.text.replace(
            "/anuncio",
            ""
        ).strip()



        if not texto:

            await message.answer(
                "Usa:\n"
                "/anuncio mensaje"
            )

            return



        enviados = 0


        for usuario in obtener_usuarios():

            try:

                await bot.send_message(
                    usuario["id"],
                    texto
                )

                enviados += 1


            except:

                pass



        await message.answer(
            f"📢 Anuncio enviado\n\n"
            f"Usuarios: {enviados}"
        )



    return bot, dp




# ==========================
# INICIAR TODOS LOS BOTS
# ==========================

async def iniciar():

    config = cargar_config()

    tareas = []


    for item in config.get(
        "bots",
        []
    ):

        if item.get(
            "activo"
        ):

            bot, dp = crear_bot(
                item["token"]
            )


            tareas.append(
                dp.start_polling(bot)
            )



    if tareas:

        await asyncio.gather(
            *tareas
        )

    else:

        print(
            "No hay bots activos"
        )




if __name__ == "__main__":

    asyncio.run(
        iniciar()
    )
