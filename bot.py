import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

user_links = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Assalomu alaykum!\n\n"
        "FastRB botiga xush kelibsiz.\n\n"
        "YouTube, TikTok, Instagram yoki Facebook link yuboring.\n\n"
        "Bot egasi:\n"
        "Baxtiyorov Behzodjon Bahodirjon o'g'li"
    )
    await update.message.reply_text(text)

async def get_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    user_links[update.message.chat_id] = url

    keyboard = [
        [InlineKeyboardButton("🎬 Video", callback_data="video")],
        [InlineKeyboardButton("🎵 MP3", callback_data="mp3")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Formatni tanlang:",
        reply_markup=reply_markup
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    data = query.data
    url = user_links.get(chat_id)

    if data == "video":

        keyboard = [
            [InlineKeyboardButton("360p", callback_data="360")],
            [InlineKeyboardButton("720p", callback_data="720")],
            [InlineKeyboardButton("1080p", callback_data="1080")]
        ]

        await query.message.reply_text(
            "Video sifatini tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "mp3":

        await query.message.reply_text("Audio yuklanmoqda...")

        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'audio.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("audio"):
                await query.message.reply_audio(audio=open(file, 'rb'))
                os.remove(file)
                break

    elif data in ["360","720","1080"]:

        await query.message.reply_text("Video yuklanmoqda...")

        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video"):
                await query.message.reply_video(video=open(file,'rb'))
                os.remove(file)
                break

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_link))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
