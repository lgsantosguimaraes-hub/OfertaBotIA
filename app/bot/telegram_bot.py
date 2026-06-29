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

# A TRAVA DE SEGURANÇA: .updater(None) impede o erro de Conflict de existir!
application = Application.builder().token(TOKEN).updater(None).build()

async def pegar_id(update, context):
    await update.message.reply_text(f"O ID deste chat é: {update.effective_chat.id}")

application.add_handler(CommandHandler("meuid", pegar_id))

@app.on_event("startup")
async def startup():
    await application.initialize()
    bot = Bot(TOKEN)
    # drop_pending_updates=True limpa a fila do Telegram na marra
    await bot.set_webhook(url=f"{WEBHOOK_URL}/webhook", drop_pending_updates=True)
    print("✅ Webhook configurado com sucesso!")

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "online", "bot": "OfertaBotIA"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)