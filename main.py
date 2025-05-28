import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from config import BOT_TOKEN
from keyboards import main_menu, subject_menu
from database import init_db, get_subjects_by_grade, get_file_by_subject
from seed_files import seed_files  # faqat 1-marta ishga tushirish uchun

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_grade = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # main.py joylashgan papka

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    first_name = message.from_user.first_name
    welcome_text = (
        f"👋 Assalomu alaykum, <b>{first_name}</b>!\n\n"
        f"📚 <b>2025-yilgi Imtihon Javoblari Botiga</b> xush kelibsiz!\n\n"
        f"Bu yerda siz o'zingizga kerakli bo'lgan fanlar bo'yicha imtihon javoblarini bepul yuklab olishingiz mumkin.\n\n"
        f"⬇️ Iltimos, sinfingizni tanlang:"
    )
    await message.answer(welcome_text, reply_markup=main_menu(), parse_mode="HTML")

@dp.message(F.text.in_(["9-sinf", "11-sinf"]))
async def grade_handler(message: types.Message):
    grade = message.text
    user_grade[message.from_user.id] = grade
    subjects = get_subjects_by_grade(grade)
    if subjects:
        await message.answer(f"{grade} uchun fanlar ro'yxati:", reply_markup=subject_menu(subjects))
    else:
        await message.answer("Hozircha bu sinf uchun materiallar mavjud emas.")

@dp.callback_query()
async def subject_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    grade = user_grade.get(user_id)

    if not grade:
        await callback.message.answer("Iltimos, avval sinfni tanlang.")
        await callback.answer()
        return

    subject = callback.data
    file_path = get_file_by_subject(grade, subject)

    print(f"[DEBUG] Bazadan olingan file_path: {file_path}")  # Bu satrni qo'shamiz

    if file_path:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(BASE_DIR, file_path)
        print(f"[DEBUG] To'liq fayl yo'li: {full_path}")

        if os.path.exists(full_path):
            # Fayl topildi
            subject_display = subject.replace("_", " ").capitalize()
            caption = (
                f"📚 Fan: {grade} {subject_display}\n"
                f"❗️Barcha Imtihon javoblarini bizning botimiz orqali bepul yuklab oling:\n\n"
                f"🔗 @imtihon_javoblari_2025robot\n"
                f"🔗 @imtihon_javoblari_2025robot"
            )
            await callback.message.answer_document(
                document=types.FSInputFile(full_path),
                caption=caption
            )
        else:
            print(f"[ERROR] Fayl topilmadi: {full_path}")  # Error log
            await callback.message.answer("Kechirasiz, fayl topilmadi.")
    else:
        print("[ERROR] Bazadan file_path topilmadi.")
        await callback.message.answer("Kechirasiz, fayl topilmadi.")

    await callback.answer()


async def main():
    init_db()
    seed_files()  # faqat bir martalik ishga tushiring (keyin olib tashlang)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
