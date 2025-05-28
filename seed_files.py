import os
from database import add_file, init_db

def seed_files():
    base_path = "files"  # files papka main.py bilan bir joyda bo'lishi kerak

    init_db()  # Bazani boshlaymiz

    for grade_folder in os.listdir(base_path):
        grade_path = os.path.join(base_path, grade_folder)

        if not os.path.isdir(grade_path):
            continue

        for filename in os.listdir(grade_path):
            # nisbiy yo'l saqlaymiz!
            relative_path = os.path.join(base_path, grade_folder, filename)
            subject = os.path.splitext(filename)[0].replace("-", " ").lower()

            add_file(grade=grade_folder, subject=subject, file_path=relative_path)
            print(f"Qo‘shildi: [{grade_folder}] {subject} → {relative_path}")

if __name__ == "__main__":
    seed_files()
