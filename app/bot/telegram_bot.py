import os
import uvicorn
from fastapi import FastAPI, Request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = "https://ofertabotia.onrender.com"

# Criando o bot sem polling
application = Application.builder().token(TOKEN).updater(None).build()

async def pegar_id(update, context):
    chat_id = update.effective_chat.id
    print(f"✅ Comando /meuid processado! ID: {chat_id}")
    await update.message.reply_text(f"O ID deste chat é: {chat_id}")

# Por enquanto, SÓ o /meuid está ativo para capturarmos o ID
application.add_handler(CommandHandler("meuid", pegar_id))

@app.on_event("startup")
async def startup():
    await application.initialize()
    await application.start() # <-- Isso liga o processamento do bot!
    bot = Bot(TOKEN)
    await bot.set_webhook(url=f"{WEBHOOK_URL}/webhook", drop_pending_updates=True)
    print("✅ Webhook configurado e Bot iniciado com sucesso!")
    webhook_info = await bot.get_webhook_info()
    print(f"DEBUG: Webhook atual no Telegram: {webhook_info.url}")
    print(f"DEBUG: Erro do último webhook: {webhook_info.last_error_message}")

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        print(f"📥 Chegou do Telegram: {data}") # Log para vermos no Render
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "online", "bot": "OfertaBotIA"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)