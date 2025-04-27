from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from flask import Flask
from threading import Thread
import os

# Flask app để giữ bot sống
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "✅ Bot is alive!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=3000)

Thread(target=run_flask).start()

# TOKEN Telegram
TOKEN = "7285284168:AAFnQ78AqqTISgul4N_5V_oiaQYhFmuPwUI"

# --- Hàm lưu chat_id không trùng ---
def save_chat_id(chat_id):
    chat_id = str(chat_id)
    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as f:
            f.write(chat_id + "\n")
    else:
        with open("users.txt", "r") as f:
            existing = f.read().splitlines()
        if chat_id not in existing:
            with open("users.txt", "a") as f:
                f.write(chat_id + "\n")

# --- Menu chính ---
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🔹 KÊNH CHÍNH THỨC", callback_data="kenh_chinh_thuc")],
        [InlineKeyboardButton("🔹 KHUYẾN MÃI MIỄN PHÍ", callback_data="uu_dai")],
        [InlineKeyboardButton("🔹 CẨM NANG THAM GIA", url="https://example.com")],
        [InlineKeyboardButton("🔹 CSKH 24/7", callback_data="ho_tro")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    save_chat_id(chat_id)
    await update.message.reply_text(
        "NEW88 kính chào quý khách, hân hạnh được hỗ trợ quý khách!",
        reply_markup=get_main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "kenh_chinh_thuc":
        keyboard = [
            [InlineKeyboardButton("✅ LINK CHÍNH THỨC", url="https://t.me/new88appbot/new88")],
            [InlineKeyboardButton("✅ KÊNH THÔNG TIN", url="https://t.me/new88_official")],
            [InlineKeyboardButton("✅ LINK NHẬP CODE", url="https://freecode-new88.pages.dev")],
            [InlineKeyboardButton("⬅️ QUAY LẠI", callback_data="main_menu")]
        ]
        await query.edit_message_text("📌 KÊNH CHÍNH THỨC:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "uu_dai":
        keyboard = [
            [InlineKeyboardButton("🎁 CHIA SẺ NHẬN CODE", url="https://t.me/new88codefree_bot")],
            [InlineKeyboardButton("📌 NHẬN CODE MỖI NGÀY", url="https://t.me/new88phatcodemienphi")],
            [InlineKeyboardButton("🔥 XEM LIVESTREAM", url="https://new88live02.pages.dev")],
            [InlineKeyboardButton("✅ LINK NHẬP CODE", url="https://freecode-new88.pages.dev")],
            [InlineKeyboardButton("⬅️ QUAY LẠI", callback_data="main_menu")]
        ]
        await query.edit_message_text("🎁 ƯU ĐÃI ĐẶC BIỆT:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "ho_tro":
        keyboard = [
            [InlineKeyboardButton("📞 LIÊN HỆ ADMIN", url="https://t.me/khieunainew88")],
            [InlineKeyboardButton("💬 LIVE CHAT", url="https://t.me/hotro_new88bot")],
            [InlineKeyboardButton("⬅️ QUAY LẠI", callback_data="main_menu")]
        ]
        await query.edit_message_text("💬 HỖ TRỢ KHÁCH HÀNG:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "main_menu":
        await query.edit_message_text(
            "NEW88 kính chào quý khách, hân hạnh được hỗ trợ quý khách!",
            reply_markup=get_main_menu()
        )

async def return_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = 5501271029  # sửa ID Admin bạn vào đây
    if update.effective_user.id != admin_id:
        return

    message = update.message

    if message.photo:
        file_id = message.photo[-1].file_id
        await message.reply_text(f"`photo_file_id`: `{file_id}`", parse_mode="Markdown")
    elif message.document:
        file_id = message.document.file_id
        await message.reply_text(f"`document_file_id`: `{file_id}`", parse_mode="Markdown")
    elif message.video:
        file_id = message.video.file_id
        await message.reply_text(f"`video_file_id`: `{file_id}`", parse_mode="Markdown")
    elif message.audio:
        file_id = message.audio.file_id
        await message.reply_text(f"`audio_file_id`: `{file_id}`", parse_mode="Markdown")
    elif message.voice:
        file_id = message.voice.file_id
        await message.reply_text(f"`voice_file_id`: `{file_id}`", parse_mode="Markdown")
    elif message.sticker:
        file_id = message.sticker.file_id
        await message.reply_text(f"`sticker_file_id`: `{file_id}`", parse_mode="Markdown")

# --- Khởi tạo Bot ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.ALL, return_file_id))

print("🤖 Bot đang chạy...")
app.run_polling()
