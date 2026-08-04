# bot.py

import asyncio
import json
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile
)

from database import (
    registrar_usuario,
    obtener_usuarios,
    guardar_pago,
    activar_vip,
    actualizar_pago
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



    # ======================
    # START
    # ======================

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




    # ======================
    # COMPRAR VIP
    # ======================

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
                photo=FSInputFile(qr), 
                caption="📷 QR Yape"
            )




    # ======================
    # RECIBIR COMPROBANTE
    # ======================

    @dp.message(
        F.photo
    )
    async def comprobante(
        message: types.Message
    ):

        config = cargar_config()


        foto = message.photo[-1]


        guardar_pago(
            message.from_user.id,
            foto.file_id
        )


        teclado = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Aprobar",
                        callback_data=f"aprobar:{message.from_user.id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Rechazar",
                        callback_data=f"rechazar:{message.from_user.id}"
                    )
                ]
            ]
        )


        for admin in config["admins"]:

            try:

                await bot.send_photo(
                    admin,
                    foto.file_id,
                    caption=(
                        "💰 Nuevo pago VIP\n\n"
                        f"Usuario ID:\n{message.from_user.id}"
                    ),
                    reply_markup=teclado
                )

            except:

                pass



        await message.answer(
            "✅ Comprobante enviado.\n"
            "Espera la aprobación."
        )




    # ======================
    # APROBAR VIP
    # ======================

    @dp.callback_query(
        F.data.startswith("aprobar:")
    )
    async def aprobar(
        call: types.CallbackQuery
    ):

        config = cargar_config()


        if call.from_user.id not in config["admins"]:
            return


        user_id = int(
            call.data.split(":")[1]
        )


        activar_vip(
            user_id
        )


        actualizar_pago(
            user_id,
            "aprobado"
        )


        await bot.send_message(
            user_id,
            "🎉 Pago aprobado\n\n"
            "💎 Bienvenido al grupo VIP:\n"
            f"{config['grupo_vip']}"
        )


        await call.message.answer(
            "✅ Usuario aprobado"
        )




    # ======================
    # RECHAZAR
    # ======================

    @dp.callback_query(
        F.data.startswith("rechazar:")
    )
    async def rechazar(
        call: types.CallbackQuery
    ):

        config = cargar_config()


        if call.from_user.id not in config["admins"]:
            return


        user_id = int(
            call.data.split(":")[1]
        )


        await bot.send_message(
            user_id,
            "❌ Tu pago fue rechazado."
        )


        await call.message.answer(
            "Pago rechazado"
        )




    # ======================
    # MI CUENTA
    # ======================

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





    # ======================
# ANUNCIOS MULTIMEDIA
# ======================

@dp.message(Command("anuncio"))
async def anuncio(message: types.Message):

    config = cargar_config()

    if message.from_user.id not in config["admins"]:
        return

    enviados = 0

    for usuario in obtener_usuarios():

        try:

            if message.photo:

                await bot.send_photo(
                    usuario["id"],
                    message.photo[-1].file_id,
                    caption=message.caption
                )

            elif message.video:

                await bot.send_video(
                    usuario["id"],
                    message.video.file_id,
                    caption=message.caption
                )

            elif message.document:

                await bot.send_document(
                    usuario["id"],
                    message.document.file_id,
                    caption=message.caption
                )

            elif message.text:

                texto = message.text.replace(
                    "/anuncio",
                    ""
                ).strip()

                await bot.send_message(
                    usuario["id"],
                    texto
                )

            enviados += 1

        except:

            pass


    await message.answer(
        f"📢 Enviado a {enviados} usuarios"
    )


    return bot, dp





async def iniciar():

    config = cargar_config()

    tareas = []


    for item in config.get(
        "bots",
        []
    ):

        if item.get("activo"):

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
