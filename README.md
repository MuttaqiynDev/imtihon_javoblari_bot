
````markdown
# 📚 Imtihon Javoblari Bot

**Telegram bot** — 2025-yilgi imtihon javoblarini sinf va fan bo‘yicha bepul taqdim etadi.

---

## ⚙️ Funksiyalar

- Foydalanuvchi o‘z sinfini tanlaydi (9-sinf, 11-sinf)
- Tanlangan sinf uchun mavjud fanlar ro‘yxati ko‘rsatiladi
- Fan tanlanganda, tegishli imtihon javobi fayli yuboriladi
- Har bir fayl bilan qo‘shimcha ma’lumot va bot linki beriladi

---

## 🛠 O‘rnatish

1. **Repository-ni klonlash:**

   ```bash
   git clone https://github.com/MuttaqiynDev/imtihon_javoblari_bot.git
   cd imtihon_javoblari_bot
````

2. **Virtual muhit yaratish va kutubxonalarni o‘rnatish:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows

   pip install -r requirements.txt
   ```

3. **`config.py` faylini yaratib, bot tokenini kiriting:**

   ```python
   BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
   ```

4. **Bazani boshlash va fayllarni qo‘shish:**

   * `seed_files.py` skriptini ishga tushiring:

   ```bash
   python seed_files.py
   ```

---

## 🚀 Ishga tushirish

```bash
python main.py
```

---

## 📁 Loyihaning asosiy fayllari

| Fayl nomi       | Vazifasi                      |
| --------------- | ----------------------------- |
| `main.py`       | Bot logikasi                  |
| `database.py`   | SQLite bazasi bilan ishlash   |
| `keyboards.py`  | Telegram klaviatura tugmalari |
| `seed_files.py` | Fayllarni bazaga yuklash      |
| `files/`        | Fan fayllari joylashgan papka |

---

## 💡 Qo‘shimcha maslahatlar

* Botni serverda doimiy ishlashi uchun `systemd` yoki `tmux` kabi vositalardan foydalaning.
* Tokenni hech qachon oshkor qilmang.
* Muammolar bo‘lsa, Issues bo‘limida xabar qoldiring.

---

© 2025 Imtihon Javoblari Bot

```


