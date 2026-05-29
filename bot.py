import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===================== SOZLAMALAR =====================
BOT_TOKEN = "8652308406:AAHrXis3KUwVUcrG3ZloGUWf8eJ7rFryZh0"
ADMIN_ID = 6471646373
KANAL_LINK = "https://t.me/+jz0EO9aFlKlkMTcy"
KURS_NOMI = "14 KUNDA AYOLLIKNI TIKLASH"
KURS_NARXI = "299 000 so'm"
KARTA_RAQAMI = "9860 3501 4975 7329"
# ======================================================

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.MARKDOWN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

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
🎁 *Narxi: 299 000 so'm*

Bir oylik kafe xarajatingizdan kam narxda —
*butun hayotingizni o'zgartiruvchi investitsiya.*

⏰ Joylar cheklangan. Ko'pchilik allaqachon boshladi.

*Siz ham tayyormisiz?* 👇
"""

def sotib_olish_tugmasi():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("💳 Sotib olish — 299 000 so'm", callback_data="sotib_olish"))
    return kb

def tasdiqlash_tugmalari(user_id):
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"tasdiqla_{user_id}"),
        InlineKeyboardButton("❌ Rad etish", callback_data=f"rad_{user_id}")
    )
    return kb

@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(KURS_TAVSIF, reply_markup=sotib_olish_tugmasi())

@dp.callback_query_handler(lambda c: c.data == "sotib_olish")
async def sotib_olish(callback: types.CallbackQuery):
    await callback.message.answer(
        f"💳 *To'lov ma'lumotlari:*\n\n"
        f"💰 Summa: *{KURS_NARXI}*\n"
        f"🏦 Karta raqami: `{KARTA_RAQAMI}`\n\n"
        f"📌 *Qadamlar:*\n"
        f"1. Yuqoridagi karta raqamiga *{KURS_NARXI}* o'tkazing\n"
        f"2. To'lov chekini (screenshot) shu yerga yuboring\n"
        f"3. Admin tasdiqlagach, kanal linki avtomatik yuboriladi ✅\n\n"
        f"⏳ Tasdiqlash vaqti: 5-30 daqiqa"
    )
    await TolovHolati.chek_kutilmoqda.set()
    await callback.answer()

@dp.message_handler(content_types=types.ContentType.PHOTO, state=TolovHolati.chek_kutilmoqda)
async def chek_qabul(message: types.Message, state: FSMContext):
    user = message.from_user
    ism = user.full_name
    username = f"@{user.username}" if user.username else "username yo'q"
    user_id = user.id

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
        reply_markup=tasdiqlash_tugmalari(user_id)
    )

    await message.answer(
        "✅ *Chekingiz qabul qilindi!*\n\n"
        "⏳ Admin tez orada tekshirib, kanal linkini yuboradi.\n"
        "Odatda 5-30 daqiqa ichida tasdiqlash bo'ladi. 🙏"
    )
    await state.finish()

@dp.message_handler(state=TolovHolati.chek_kutilmoqda)
async def chek_xato(message: types.Message):
    await message.answer("📸 Iltimos, *to'lov chekining rasmini* yuboring (screenshot).")

@dp.callback_query_handler(lambda c: c.data.startswith("tasdiqla_"))
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
            )
        )
        await callback.message.edit_caption(
            callback.message.caption + "\n\n✅ *TASDIQLANDI — link yuborildi*"
        )
    except Exception as e:
        await callback.message.answer(f"Xatolik: {e}")
    await callback.answer("✅ Tasdiqlandi!")

@dp.callback_query_handler(lambda c: c.data.startswith("rad_"))
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
            )
        )
        await callback.message.edit_caption(
            callback.message.caption + "\n\n❌ *RAD ETILDI*"
        )
    except Exception as e:
        await callback.message.answer(f"Xatolik: {e}")
    await callback.answer("❌ Rad etildi!")

if __name__ == "__main__":
    print("Bot ishga tushdi! ✅")
    executor.start_polling(dp, skip_updates=True)
    
