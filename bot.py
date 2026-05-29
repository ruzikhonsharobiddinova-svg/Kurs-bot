import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# ===================== SOZLAMALAR =====================
BOT_TOKEN = "8652308406:AAHrXis3KUwVUcrG3ZloGUWf8eJ7rFryZh0"
ADMIN_ID = 6471646373
KANAL_LINK = "https://t.me/+jz0EO9aFlKlkMTcy"
KURS_NOMI = "14 KUNDA AYOLLIKNI TIKLASH"
KURS_NARXI = "299 000 so'm"
KARTA_RAQAMI = "9860 3501 4975 7329"
# ======================================================

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class TolovHolati(StatesGroup):
    chek_kutilmoqda = State()

KURS_TAVSIF = """
🌸 *14 KUNDA AYOLLIKNI TIKLASH*

_"Men charchadim... lekin nima uchun charchaganim ham esimda yo'q"_

Bu so'zlar tanish emasmi? 💭

Har kuni hammaga kuch berasiz — farzandlarga, erga, ishga, do'stlarga...
Lekin *o'zingizga* qachon kuch berdingiz?

━━━━━━━━━━━━━━━━━━━━
*Siz bu kursga kerak bo'lgan ayolsiz, agar:*

✦ Ertalab ko'zingizni ochib, yorqinlik his qilmayotgan bo'lsangiz
✦ "Ayol" ekanligingizni emas, faqat "ona", "xotin", "xodim" ekanligingizni his qilsangiz
✦ O'zingizni sevish nima ekanini unutib qo'ygan bo'lsangiz
✦ Hayotda biror narsa yetishmayapti — lekin nima ekanini bilmasangiz

━━━━━━━━━━━━━━━━━━━━
🔑 *14 kun ichida nima o'zgaradi?*

💎 Ayollik energiyangiz uyg'onadi
💎 O'zingizga qaytasiz — haqiqiy, kuchli, go'zal
💎 Munosabatlardagi sovuqlik o'rniga iliqlik paydo bo'ladi
💎 Hayotga yangi ko'z bilan qaray boshlaysiz
💎 Ichki tinchlik va o'z-o'ziga ishonch tiklanadi

━━━━━━━━━━━━━━━━━━━━
⚡️ *Bu kurs boshqalardan farqi:*

Bu yerda nazariya yo'q.
Faqat *amaliyot, his va o'zgarish.*

Har kun — 1 topshiriq.
Har topshiriq — yangi "men"ga bir qadam.

━━━━━━━━━━━━━━━━━━━━
🎁 *Narxi: 299 000 so'm*

Bir oylik kafe xarajatingizdan kam narxda —
*butun hayotingizni o'zgartiruvchi investitsiya.*

⏰ Joylar cheklangan. Ko'pchilik allaqachon boshladi.

*Siz ham tayyormisiz?* 👇
"""

def sotib_olish_tugmasi():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Sotib olish — 299 000 so'm", callback_data="sotib_olish")]
    ])

def tasdiqlash_tugmalari(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"tasdiqla_{user_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"rad_{user_id}")
        ]
    ])

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        KURS_TAVSIF,
        parse_mode="Markdown",
        reply_markup=sotib_olish_tugmasi()
    )

@dp.callback_query(F.data == "sotib_olish")
async def sotib_olish(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        f"💳 *To'lov ma'lumotlari:*\n\n"
        f"💰 Summa: *{KURS_NARXI}*\n"
        f"🏦 Karta raqami: `{KARTA_RAQAMI}`\n\n"
        f"📌 *Qadamlar:*\n"
        f"1. Yuqoridagi karta raqamiga *{KURS_NARXI}* o'tkazing\n"
        f"2. To'lov chekini (screenshot) shu yerga yuboring\n"
        f"3. Admin tasdiqlagach, kanal linki avtomatik yuboriladi ✅\n\n"
        f"⏳ Tasdiqlash vaqti: 5-30 daqiqa",
        parse_mode="Markdown"
    )
    await state.set_state(TolovHolati.chek_kutilmoqda)
    await callback.answer()

@dp.message(TolovHolati.chek_kutilmoqda, F.photo)
async def chek_qabul(message: types.Message, state: FSMContext):
    user = message.from_user
    ism = user.full_name
    username = f"@{user.username}" if user.username else "username yo'q"
    user_id = user.id

    # Adminga xabar yuborish
    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=(
            f"💰 *Yangi to'lov cheki!*\n\n"
            f"👤 Ism: {ism}\n"
            f"🆔 ID: `{user_id}`\n"
            f"📱 Username: {username}\n\n"
            f"Kurs: *{KURS_NOMI}*\n"
            f"Narx: *{KURS_NARXI}*"
        ),
        parse_mode="Markdown",
        reply_markup=tasdiqlash_tugmalari(user_id)
    )

    await message.answer(
        "✅ *Chekingiz qabul qilindi!*\n\n"
        "⏳ Admin tez orada tekshirib, kanal linkini yuboradi.\n"
        "Odatda 5-30 daqiqa ichida tasdiqlash bo'ladi. 🙏",
        parse_mode="Markdown"
    )
    await state.clear()

@dp.message(TolovHolati.chek_kutilmoqda)
async def chek_xato(message: types.Message):
    await message.answer(
        "📸 Iltimos, *to'lov chekining rasmini* yuboring (screenshot).",
        parse_mode="Markdown"
    )

# Admin: tasdiqlash
@dp.callback_query(F.data.startswith("tasdiqla_"))
async def tasdiqla(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    try:
        await bot.send_message(
            chat_id=user_id,
            text=(
                f"🎉 *Tabriklaymiz! To'lovingiz tasdiqlandi!*\n\n"
                f"Quyidagi link orqali maxfiy kanalga kiring:\n\n"
                f"🔗 {KANAL_LINK}\n\n"
                f"💎 *{KURS_NOMI}* kursiga xush kelibsiz!\n"
                f"O'zgarishlar sizni kutmoqda. 🌸"
            ),
            parse_mode="Markdown"
        )
        await callback.message.edit_caption(
            callback.message.caption + "\n\n✅ *TASDIQLANDI — link yuborildi*",
            parse_mode="Markdown"
        )
    except Exception as e:
        await callback.message.answer(f"Xatolik: {e}")
    await callback.answer("✅ Tasdiqlandi!")

# Admin: rad etish
@dp.callback_query(F.data.startswith("rad_"))
async def rad_et(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[1])
    try:
        await bot.send_message(
            chat_id=user_id,
            text=(
                "❌ *Afsuski, to'lovingiz tasdiqlanmadi.*\n\n"
                "Sabab: chek aniq ko'rinmagan yoki to'lov topilmagan.\n\n"
                "📞 Muammo bo'lsa admin bilan bog'laning yoki qayta to'lov qiling.\n"
                "/start — qaytadan boshlash"
            ),
            parse_mode="Markdown"
        )
        await callback.message.edit_caption(
            callback.message.caption + "\n\n❌ *RAD ETILDI*",
            parse_mode="Markdown"
        )
    except Exception as e:
        await callback.message.answer(f"Xatolik: {e}")
    await callback.answer("❌ Rad etildi!")

async def main():
    print("Bot ishga tushdi! ✅")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
