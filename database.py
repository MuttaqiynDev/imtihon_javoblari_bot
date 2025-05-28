import sqlite3

DB_NAME = "bot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Fayllar jadvalini yaratamiz (agar mavjud bo'lmasa)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grade TEXT NOT NULL,
            subject TEXT NOT NULL,
            file_path TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def get_subjects_by_grade(grade):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Berilgan sinf uchun barcha fanlarni topamiz
    cursor.execute("SELECT DISTINCT subject FROM files WHERE grade = ?", (grade,))
    result = cursor.fetchall()

    conn.close()
    return [row[0] for row in result]

def get_file_by_subject(grade, subject):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Berilgan sinf va fan uchun fayl manzilini topamiz
    cursor.execute("SELECT file_path FROM files WHERE grade = ? AND subject = ?", (grade, subject))
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else None

# Fayllarni qo‘shish uchun (admin interfeysda ishlatish mumkin)
def add_file(grade, subject, file_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO files (grade, subject, file_path) VALUES (?, ?, ?)",
        (grade, subject, file_path)
    )

    conn.commit()
    conn.close()
