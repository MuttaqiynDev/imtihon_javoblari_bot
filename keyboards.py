from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Asosiy menyu (9-sinf, 11-sinf)
def main_menu():
    buttons = [
        [KeyboardButton(text="9-sinf")],
        [KeyboardButton(text="11-sinf")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Ortga va bosh menyu tugmalari (kelajakda ishlatilishi mumkin)
def back_menu():
    buttons = [
        [KeyboardButton(text="◀️ Ortga")],
        [KeyboardButton(text="🏠 Bosh menyu")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Fanlar ro‘yxatidan inline tugmalar yasash
def subject_menu(subjects: list[str]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=subject,
                callback_data=subject.lower().replace(" ", "_")[:64]  # xavfsiz format
            )
        ] for subject in subjects
    ])
    return markup
