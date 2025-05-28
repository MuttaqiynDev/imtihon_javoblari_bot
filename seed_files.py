import os
from database import add_file, init_db

def seed_files():
    base_path = "files"
    init_db()  # Bazani boshlaymiz

    for grade_folder in os.listdir(base_path):
        grade_path = os.path.join(base_path, grade_folder)

        if not os.path.isdir(grade_path):
            continue

        for filename in os.listdir(grade_path):
            file_path = os.path.join(grade_path, filename)

            # Fayl nomidan subject ni ajratamiz (masalan, "algebra.pdf" → "algebra")
            subject = os.path.splitext(filename)[0].replace("-", " ").replace("_", " ").lower()

            # Qo'shilayotgan file_path nisbiy bo'lishi kerak, ya'ni files/9-sinf/algebra.pdf ko'rinishida
            relative_path = os.path.relpath(file_path)

            add_file(grade=grade_folder, subject=subject, file_path=relative_path)
            print(f"Qo‘shildi: [{grade_folder}] {subject} → {relative_path}")

if __name__ == "__main__":
    seed_files()
