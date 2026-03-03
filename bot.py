import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8080))
RAILWAY_URL = os.environ.get("RAILWAY_STATIC_URL")

subjects = [
    "Biochemistry",
    "Histology",
    "Embryology",
    "Gross",
    "Physiology",
    "English",
    "Ethics"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(sub, callback_data=sub)] for sub in subjects]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 اختر المادة:", reply_markup=reply_markup)

async def subject_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject = query.data

    keyboard = [
        [InlineKeyboardButton("📖 Online Sheets", callback_data="online")],
        [InlineKeyboardButton("🏫 Offline Sheets", callback_data="offline")],
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"{subject} - اختر النوع:", reply_markup=reply_markup)

async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton(sub, callback_data=sub)] for sub in subjects]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("📚 اختر المادة:", reply_markup=reply_markup)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(back_handler, pattern="back"))
app.add_handler(CallbackQueryHandler(subject_handler))

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=f"https://{RAILWAY_URL}"
)
