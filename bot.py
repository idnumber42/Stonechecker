import os
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram import Update

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото получено")

if __name__ == '__main__':
    import asyncio

    async def main():
        app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

        await app.bot.set_webhook(os.getenv("WEBHOOK_URL"))

        await app.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)),
            webhook_url=os.getenv("WEBHOOK_URL")
        )

    asyncio.run(main())
