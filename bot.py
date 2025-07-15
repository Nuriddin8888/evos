# bot.py (aiogram v3)
import os
import django
import asyncio
from asgiref.sync import sync_to_async

from aiogram import Bot, Dispatcher, F
from aiogram.types import CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from products.models import Cart

BOT_TOKEN = "7074013206:AAHTj2_4Yu6tdM37UFkCuGZtW7owv2MBtWI"
ADMIN_CHAT_ID = 7149602547 

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.callback_query(F.data.startswith("confirm_order_"))
async def confirm_order_handler(callback: CallbackQuery):
    cart_id = callback.data.split("_")[-1]

    cart = await sync_to_async(lambda: Cart.objects.filter(id=cart_id).first())()

    if cart:
        cart.is_ordered = True
        await sync_to_async(cart.save)()
        await callback.message.edit_text(
            callback.message.text + "\n\n✅ Buyurtma tasdiqlandi!"
        )
        await callback.answer("Tasdiqlandi ✅")
    else:
        await callback.answer("❌ Buyurtma topilmadi")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
