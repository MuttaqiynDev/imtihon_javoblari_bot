import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from config import BOT_TOKEN
from keyboards import main_menu, subject_menu
from database import init_db, get_subjects_by_grade, get_file_by_subject  # faqat 1-marta ishga tushirish uchun
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from flask import Flask


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_grade = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # main.py joylashgan papka

# ==============================
# 1) SET UP FLASK SERVER
# ==============================
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET", "HEAD"])
def home():
    return "OK", 200

@flask_app.route("/ping", methods=["GET", "HEAD"])
def ping():
    return "OK", 200

@flask_app.route("/healthz", methods=["GET", "HEAD"])
def healthz():
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", "5000"))
    flask_app.run(host="0.0.0.0", port=port, use_reloader=False, threaded=True)

# ==============================
# 2) TELEGRAM BOT FUNCTIONALITY
# ==============================
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
        file_path = file_path.replace("\\", "/")
        full_path = os.path.join(BASE_DIR, file_path)
        print(f"[DEBUG] To'liq fayl yo'li: {full_path}")

        if os.path.exists(full_path):
            subject_display = subject.replace("_", " ").capitalize()
            caption = (
                f"📚 Fan: {subject_display}\n"
                f"❗️Barcha Imtihon javoblarini bizning botimiz orqali bepul yuklab oling:\n\n"
                f"🔗 @imtihon_javoblari_2025robot\n"
                f"🔗 @imtihon_javoblari_2025robot"
            )
            await callback.message.answer_document(
                document=types.FSInputFile(full_path),
                caption=caption
            )
        else:
            print(f"[ERROR] Fayl topilmadi: {full_path}")
            await callback.message.answer("Kechirasiz, fayl topilmadi.")
    else:
        print("[ERROR] Bazadan file_path topilmadi.")
        await callback.message.answer("Kechirasiz, fayl topilmadi.")

    await callback.answer()

async def main():
    init_db()
    # seed_files()  # faqat bir marta

    # Start Flask server in a separate thread
    class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"AFK bot is alive!")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def start_dummy_server():
    port = int(os.environ.get("PORT", 10000))  # Render injects this
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    print(f"Dummy server listening on port {port}")
    server.serve_forever()

    

    # Start Telegram bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    threading.Thread(target=start_dummy_server, daemon=True).start()

    asyncio.run(main())
