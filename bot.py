# bot.py

import asyncio
import json

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import registrar_usuario, obtener_usuarios


CONFIG_FILE = "config.json"


def cargar_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def menu_usuario():

    config = cargar_config()

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Grupo Público",
                    url=config["grupo_publico"]
                )
            ],
            [
                InlineKeyboardButton(
                    text="💎 Comprar VIP S/20",
                    callback_data="comprar_vip"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👤 Mi Cuenta",
                    callback_data="cuenta"
                )
            ]
        ]
    )


def crear_bot(token):

    bot = Bot(token=token)
    dp = Dispatcher()


    # Usuario entra al bot
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


    # Comprar VIP
    @dp.callback_query(F.data == "comprar_vip")
    async def comprar_vip(call: types.CallbackQuery):

        config = cargar_config()

        await call.message.answer(
            "💎 Compra VIP\n\n"
            "Precio: S/ 20\n\n"
            "Realiza el pago por Yape y envía tu comprobante."
        )

        if config.get("qr_yape"):
            await call.message.answer_photo(
                config["qr_yape"]
            )


    # Mi cuenta
    @dp.callback_query(F.data == "cuenta")
    async def cuenta(call: types.CallbackQuery):

        await call.message.answer(
            f"👤 Tu ID:\n{call.from_user.id}"
        )


    # Anuncio solo administradores
    @dp.message(Command("anuncio"))
    async def anuncio(message: types.Message):

        config = cargar_config()

        if message.from_user.id not in config["admins"]:
            return


        texto = message.text.replace(
            "/anuncio",
            ""
        ).strip()


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
            f"📢 Anuncio enviado\n"
            f"Usuarios: {enviados}"
        )


    return bot, dp



async def iniciar():

    config = cargar_config()

    tareas = []


    for item in config["bots"]:

        if item["activo"]:

            bot, dp = crear_bot(
                item["token"]
            )

            tareas.append(
                dp.start_polling(bot)
            )


    await asyncio.gather(*tareas)



if __name__ == "__main__":
    asyncio.run(iniciar())
