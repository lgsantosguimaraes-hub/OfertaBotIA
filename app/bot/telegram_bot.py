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
# Verifique se esta URL está exatamente igual à do seu serviço no Render
WEBHOOK_URL = "https://ofertabotia.onrender.com" 

application = Application.builder().token(TOKEN).build()

# Função que força o envio do ID
async def pegar_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"DEBUG: O ID do chat que enviou a mensagem é: {chat_id}")
    await update.message.reply_text(f"O ID deste chat é: {chat_id}")

application.add_handler(CommandHandler("meuid", pegar_id))

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
    bot = Bot(TOKEN)
    # Tenta definir o webhook
    await bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    
    await application.initialize()
    await application.start()

    config = uvicorn.Config(app=app_web, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
    server = uvicorn.Server(config)
    
    print("🚀 Bot rodando via Webhook!")
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())