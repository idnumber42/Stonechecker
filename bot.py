import os
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import openai
import base64

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def handle_photo(update: Update, context: CallbackContext):
    photo = update.message.photo[-1]
    file = context.bot.get_file(photo.file_id)
    file_path = f"/tmp/{photo.file_unique_id}.jpg"
    file.download(file_path)

    with open(file_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "На фото изображён камень. Назови его тип, если возможно, и опиши свойства."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]}
        ]
    )

    text_response = response.choices[0].message["content"].strip()
    update.message.reply_text(text_response)

if __name__ == "__main__":
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
    updater.start_polling()
    updater.idle()