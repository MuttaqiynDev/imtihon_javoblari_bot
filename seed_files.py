import os
from database import add_file, init_db

def seed_files():
    base_path = "files"  # Fayllar papkasi main.py joylashgan joyda

    init_db()  # Bazani yaratamiz yoki ochamiz

    for grade_folder in os.listdir(base_path):
        grade_path = os.path.join(base_path, grade_folder)
        if not os.path.isdir(grade_path):
            continue

        for filename in os.listdir(grade_path):
            # Fayl uchun nisbiy yo'lni to'g'ri saqlaymiz
            relative_path = os.path.join(base_path, grade_folder, filename)
            subject = os.path.splitext(filename)[0].replace("-", " ").lower()

            print(f"[SEED] Qo'shilyapti: {grade_folder} | {subject} | {relative_path}")
            add_file(grade=grade_folder, subject=subject, file_path=relative_path)

if __name__ == "__main__":
    seed_files()
