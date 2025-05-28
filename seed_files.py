import os
from database import add_file, init_db

def seed_files():
    """Fayllar papkasidagi barcha fayllarni bazaga qo'shish"""
    base_path = "files"  # Fayllar papkasi main.py joylashgan joyda

    # Tekshirish: files papkasi bor-yo'qligi
    if not os.path.exists(base_path):
        print(f"❌ [SEED ERROR] '{base_path}' papkasi topilmadi!")
        print("Iltimos, quyidagi struktura yarating:")
        print("files/")
        print("├── 9-sinf/")
        print("│   ├── matematika.pdf")
        print("│   └── fizika.pdf")
        print("└── 11-sinf/")
        print("    ├── matematika.pdf")
        print("    └── fizika.pdf")
        return

    init_db()  # Bazani yaratamiz yoki ochamiz
    
    total_files = 0
    added_files = 0

    print("🚀 [SEED] Fayllarni bazaga yuklash boshlandi...")

    for grade_folder in os.listdir(base_path):
        grade_path = os.path.join(base_path, grade_folder)
        
        # Faqat papkalarni tekshiramiz
        if not os.path.isdir(grade_path):
            print(f"⚠️  [SEED WARNING] '{grade_folder}' papka emas, o'tkazib yuborildi")
            continue

        print(f"📁 [SEED] '{grade_folder}' papkasi tekshirilmoqda...")

        files_in_grade = 0
        for filename in os.listdir(grade_path):
            file_full_path = os.path.join(grade_path, filename)
            
            # Faqat fayllarni olامiz, papkalarni emas
            if not os.path.isfile(file_full_path):
                continue
            
            # Fayl hajmini tekshiramiz
            file_size = os.path.getsize(file_full_path)
            if file_size > 50 * 1024 * 1024:  # 50MB
                print(f"⚠️  [SEED WARNING] '{filename}' juda katta ({file_size/1024/1024:.1f}MB), o'tkazib yuborildi")
                continue

            # Ruxsat etilgan formatlarni tekshiramiz
            allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.zip', '.rar', '.jpg', '.png']
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext not in allowed_extensions:
                print(f"⚠️  [SEED WARNING] '{filename}' ruxsat etilmagan format ({file_ext}), o'tkazib yuborildi")
                continue

            # Fayl uchun nisbiy yo'lni to'g'ri saqlaymiz
            relative_path = os.path.join(base_path, grade_folder, filename)
            
            # Subject nomini yaratish
            subject_name = os.path.splitext(filename)[0]  # .pdf, .doc kabi kengaytmalarni olib tashlaymiz
            
            # Maxsus belgilarni almashtirish
            subject_name = subject_name.replace("-", " ").replace("_", " ")
            subject_name = subject_name.lower().strip()
            
            # Bo'sh subject nomlarini oldini olish
            if not subject_name:
                subject_name = "unknown"

            print(f"  📄 [SEED] Fayl: {filename}")
            print(f"      Sinf: {grade_folder}")
            print(f"      Fan: {subject_name}")
            print(f"      Yo'l: {relative_path}")
            print(f"      Hajm: {file_size/1024:.1f} KB")

            # Bazaga qo'shish
            try:
                add_file(grade=grade_folder, subject=subject_name, file_path=relative_path)
                added_files += 1
                files_in_grade += 1
            except Exception as e:
                print(f"❌ [SEED ERROR] {filename} qo'shishda xatolik: {e}")

            total_files += 1

        print(f"✅ [SEED] '{grade_folder}' papkasidan {files_in_grade} ta fayl qo'shildi\n")

    print("=" * 50)
    print(f"🎉 [SEED COMPLETE] Jami: {total_files} ta fayl tekshirildi")
    print(f"✅ [SEED COMPLETE] Qo'shildi: {added_files} ta fayl")
    print(f"⚠️  [SEED COMPLETE] O'tkazib yuborildi: {total_files - added_files} ta fayl")
    print("=" * 50)

def clear_database():
    """Bazani tozalash (test uchun)"""
    import sqlite3
    
    conn = sqlite3.connect("exam_bot.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM files")
    conn.commit()
    conn.close()
    print("🧹 [CLEAR] Baza tozalandi!")

if __name__ == "__main__":
    print("1. Bazani tozalash va qayta yuklash")
    print("2. Faqat yangi fayllarni qo'shish")
    choice = input("Tanlang (1/2): ")
    
    if choice == "1":
        clear_database()
        seed_files()
    else:
        seed_files()