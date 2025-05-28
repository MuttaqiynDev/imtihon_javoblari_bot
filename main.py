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

# Foydalanuvchilar sinfini saqlash uchun
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
    
    print(f"[DEBUG] Foydalanuvchi {message.from_user.id} {grade}ni tanladi")
    
    subjects = get_subjects_by_grade(grade)
    
    if subjects:
        subjects_text = "\n".join([f"• {subject}" for subject in subjects])
        response_text = f"📚 <b>{grade}</b> uchun mavjud fanlar:\n\n{subjects_text}\n\n👇 Kerakli fanni tanlang:"
        await message.answer(response_text, reply_markup=subject_menu(subjects), parse_mode="HTML")
    else:
        await message.answer(f"❌ Kechirasiz, <b>{grade}</b> uchun hozircha materiallar mavjud emas.", parse_mode="HTML")

@dp.callback_query()
async def subject_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    grade = user_grade.get(user_id)

    if not grade:
        await callback.message.answer("❌ Iltimos, avval sinfni tanlang.\n\n/start buyrug'ini bosing.")
        await callback.answer()
        return

    subject = callback.data
    print(f"[DEBUG] Foydalanuvchi: {user_id}, Sinf: {grade}, Fan: {subject}")
    
    file_path = get_file_by_subject(grade, subject)
    print(f"[DEBUG] Bazadan olingan file_path: {file_path}")

    if file_path:
        full_path = os.path.join(BASE_DIR, file_path)
        print(f"[DEBUG] To'liq fayl yo'li: {full_path}")

        if os.path.exists(full_path):
            # Fayl topildi va yuborilmoqda
            subject_display = subject.replace("_", " ").title()
            caption = (
                f"📚 <b>Fan:</b> {grade} {subject_display}\n\n"
                f"✅ Fayl muvaffaqiyatli yuklandi!\n\n"
                f"❗️ Barcha imtihon javoblarini bizning botimiz orqali bepul yuklab oling:\n\n"
                f"🔗 @imtihon_javoblari_2025robot\n"
                f"🔗 @imtihon_javoblari_2025robot"
            )
            
            try:
                await callback.message.answer_document(
                    document=types.FSInputFile(full_path),
                    caption=caption,
                    parse_mode="HTML"
                )
                print(f"[SUCCESS] Fayl yuborildi: {subject_display}")
            except Exception as e:
                print(f"[ERROR] Fayl yuborishda xatolik: {e}")
                await callback.message.answer("❌ Faylni yuborishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.")
        else:
            print(f"[ERROR] Fayl topilmadi: {full_path}")
            await callback.message.answer("❌ Kechirasiz, fayl topilmadi yoki olib tashlangan.")
    else:
        print(f"[ERROR] Bazadan file_path topilmadi: {grade} | {subject}")
        await callback.message.answer("❌ Kechirasiz, bu fan uchun fayl mavjud emas.")

    await callback.answer()

# Noma'lum xabarlar uchun handler
@dp.message()
async def unknown_message_handler(message: types.Message):
    await message.answer(
        "❓ Kechirasiz, men sizni tushunmadim.\n\n"
        "Iltimos, quyidagi tugmalardan foydalaning yoki /start buyrug'ini bosing.",
        reply_markup=main_menu()
    )

async def main():
    print("[BOT] Bot ishga tushmoqda...")
    
    # Ma'lumotlar bazasini ishga tushirish
    init_db()
    
    # Fayllarni bazaga yuklash (faqat birinchi marta)
    # Agar kerak bo'lsa, quyidagi satrni izohdan chiqaring:
    # seed_files()
    
    print("[BOT] Bot tayyor! Polling boshlanmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())