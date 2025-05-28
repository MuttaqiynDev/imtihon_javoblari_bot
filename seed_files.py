import os
from database import add_file, init_db

def seed_files():
    base_path = "files"
    init_db()

    for grade_folder in os.listdir(base_path):
        grade_path = os.path.join(base_path, grade_folder)

        if not os.path.isdir(grade_path):
            continue

        for filename in os.listdir(grade_path):
            # Nisbiy fayl yo'li bazaga saqlanadi: files/9-sinf/algebra.pdf
            relative_path = os.path.join("files", grade_folder, filename)


            subject = os.path.splitext(filename)[0].replace("-", "_").lower()

            add_file(grade=grade_folder, subject=subject, file_path=relative_path)
            print(f"Qo‘shildi: [{grade_folder}] {subject} → {relative_path}")

if __name__ == "__main__":
    seed_files()
