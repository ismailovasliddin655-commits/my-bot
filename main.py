import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ChatMemberStatus

# 1. BOT TOKENINGIZ
BOT_TOKEN = "8742217058:AAGSMXc36z9wIK-YrXuCPo-aXuy-ZxU5om8"

# 2. MAJBURIY A'ZO BO'LADIGAN TELEGRAM KANAL
REQUIRED_CHANNEL = "@fsgame2022" 

# 3. IJTIMOIY TARMOQLAR LINKLARI
INSTAGRAM_LINK = "https://instagram.com"
YOUTUBE_LINK = "https://youtube.com"

# 4. O'YINLAR BAZASI (Kod va uning linki)
GAMES_DATABASE = {
    "101": "https://t.me",  
    "102": "https://t.me",  
    "fs20": "https://t.me"  
}

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Telegram kanalga a'zolikni tekshirish funksiyasi
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            return True
        return False
    except Exception:
        return False

# /start buyrug'i kelganda
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    is_subscribed = await check_subscription(message.from_user.id)
    
    if is_subscribed:
        await message.answer(
            f"Salom {message.from_user.full_name}! Barcha obunalar tasdiqlandi. 🎉\n\n"
            "O'yinni yuklab olish uchun uning maxsus kodini yuboring. 🎮"
        )
    else:
        builder = InlineKeyboardBuilder()
        # LINK SHU YERDA TO'G'RILANDI (slash belgisi qo'shildi)
        tg_link = f"https://t.me{REQUIRED_CHANNEL.replace('@', '')}"
        
        builder.button(text="1. Telegram kanalga a'zo bo'lish 🚀", url=tg_link)
        builder.button(text="2. Instagramga obuna bo'lish 📸", url=INSTAGRAM_LINK)
        builder.button(text="3. YouTubega obuna bo'lish 🔴", url=YOUTUBE_LINK)
        builder.button(text="A'zo bo'ldim va tekshirish ✅", callback_data="check_sub")
        builder.adjust(1)
        
        await message.answer(
            f"Salom {message.from_user.full_name}!\n\n"
            "Botdan foydalanish va o'yinlarni yuklab olish uchun quyidagi sahifalarimizga obuna bo'lishingiz shart:\n\n"
            "👇 Pastdagi tugmalar orqali o'ting:",
            reply_markup=builder.as_markup()
        )

# "A'zo bo'ldim va tekshirish" tugmasi bosilganda
@dp.callback_query(lambda c: c.data == "check_sub")
async def check_callback(callback: types.CallbackQuery):
    is_subscribed = await check_subscription(callback.from_user.id)
    if is_subscribed:
        await callback.message.delete()
        await callback.message.answer(
            "Rahmat! A'zolik muvaffaqiyatli tasdiqlandi. ✅\n"
            "Endi o'zingizga yoqqan o'yin kodini yuborishingiz mumkin! 🎮"
        )
    else:
        await callback.answer(
            "Siz hali Telegram kanalimizga a'zo bo'lmadingiz! ❌\n"
            "Iltimos, kanalga a'zo bo'lib keyin tekshiring.", 
            show_alert=True
        )

# Foydalanuvchi kod yuborganda o'yinni topish
@dp.message()
async def send_game(message: types.Message):
    is_subscribed = await check_subscription(message.from_user.id)
    
    if not is_subscribed:
        await start_cmd(message)
        return

    game_code = message.text.strip()
    
    if game_code in GAMES_DATABASE:
        game_link = GAMES_DATABASE[game_code]
        await message.answer(
            f"🎮 Siz so'ragan o'yin topildi!\n\n"
            f"👇 Yuklab olishomiz uchun pastdagi linkka bosing:\n{game_link}"
        )
    else:
        await message.answer(
            "❌ Noto'g'ri kod yubordingiz yoki bunday o'yin hali bazamizga qo'shilmagan.\n"
            "Iltimos, kodni tekshirib qaytadan yuboring. 🔄"
        )

if __name__ == "__main__":
    dp.run_polling(bot)
