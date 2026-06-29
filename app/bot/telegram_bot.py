import os
import asyncio
import uvicorn
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

app_web = FastAPI()
TOKEN = os.getenv("TELEGRAM_TOKEN")
# URL que o Render te deu (substitua pelo seu link do Render)
WEBHOOK_URL = "https://ofertabotia.onrender.com" 

# --- CONFIGURAÇÃO DO BOT ---
application = Application.builder().token(TOKEN).build()

@app_web.post("/webhook")
async def webhook(request: Request):
    update_data = await request.json()
    update = Update.de_json(update_data, application.bot)
    await application.process_update(update)
    return {"status": "ok"}

@app_web.get("/")
async def read_root():
    return {"status": "online"}

async def main():
    # Configura o Webhook no Telegram
    bot = Bot(TOKEN)
    await bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    
    # Handlers
    async def pegar_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"O ID deste chat é: {update.effective_chat.id}")
    
    application.add_handler(CommandHandler("meuid", pegar_id))
    
    await application.initialize()
    await application.start()

    # Roda o servidor Web usando o Uvicorn
    config = uvicorn.Config(app=app_web, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
    server = uvicorn.Server(config)
    
    print("🚀 Bot rodando via Webhook!")
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())