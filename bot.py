import os
import openai
import base64
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

openai.api_key = os.getenv("OPENAI_API_KEY")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    file_path = f"/tmp/{photo.file_unique_id}.jpg"
    await file.download_to_drive(file_path)

    with open(file_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "На фото изображён камень. Назови его тип, если возможно, и опиши свойства."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]}
        ]
    )

    reply = response.choices[0].message.content.strip()
    await update.message.reply_text(reply)

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.run_polling()