import sqlite3
import os

# Database fayl nomi
DB_FILE = "exam_bot.db"

def init_db():
    """Ma'lumotlar bazasini yaratish va jadvallarni sozlash"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Files jadvali yaratish
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grade TEXT NOT NULL,
            subject TEXT NOT NULL,
            file_path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[DB] Ma'lumotlar bazasi tayyor!")

def add_file(grade: str, subject: str, file_path: str):
    """Bazaga yangi fayl ma'lumotini qo'shish"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Avval bunday fayl bor-yo'qligini tekshiramiz
    cursor.execute('''
        SELECT id FROM files WHERE grade = ? AND subject = ? AND file_path = ?
    ''', (grade, subject, file_path))
    
    if cursor.fetchone() is None:
        # Fayl mavjud emas, qo'shamiz
        cursor.execute('''
            INSERT INTO files (grade, subject, file_path) VALUES (?, ?, ?)
        ''', (grade, subject, file_path))
        conn.commit()
        print(f"[DB] Qo'shildi: {grade} | {subject} | {file_path}")
    else:
        print(f"[DB] Allaqachon mavjud: {grade} | {subject}")
    
    conn.close()

def get_subjects_by_grade(grade: str) -> list:
    """Berilgan sinf uchun mavjud fanlar ro'yxatini olish"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT DISTINCT subject FROM files WHERE grade = ?
    ''', (grade,))
    
    results = cursor.fetchall()
    conn.close()
    
    # Subject nomlarini chiroyli formatga o'tkazish
    subjects = []
    for row in results:
        subject_name = row[0].replace("_", " ").title()
        subjects.append(subject_name)
    
    return subjects

def get_file_by_subject(grade: str, subject: str) -> str:
    """Sinf va fan bo'yicha fayl yo'lini olish"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Subject nomini bazadagi formatga o'tkazish
    subject_db_format = subject.lower().replace(" ", "_")
    
    cursor.execute('''
        SELECT file_path FROM files WHERE grade = ? AND subject = ?
    ''', (grade, subject_db_format))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    else:
        return None

def get_all_files():
    """Barcha fayllar ro'yxatini olish (debug uchun)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM files')
    results = cursor.fetchall()
    conn.close()
    
    return results

if __name__ == "__main__":
    # Test uchun
    init_db()
    files = get_all_files()
    print("Bazadagi barcha fayllar:")
    for file in files:
        print(file)