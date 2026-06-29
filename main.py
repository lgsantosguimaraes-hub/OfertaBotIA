import os
import logging
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from telegram import Update
from telegram.ext import Application, CommandHandler

# Import handlers
from app.bot.handlers import start, carregar_ofertas

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://ofertabotia.onrender.com").strip()

if not TOKEN:
    raise RuntimeError("❌ TELEGRAM_TOKEN não encontrado no .env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 60)
    logger.info("🚀 INICIANDO OFERTABOT IA")
    logger.info("=" * 60)

    application = Application.builder().token(TOKEN).updater(None).build()
    app.state.application = application

    await application.initialize()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("carregar", carregar_ofertas))
    application.add_handler(CommandHandler("meuid", lambda u, c: u.message.reply_text(f"ID: `{u.effective_chat.id}`", parse_mode="MarkdownV2")))

    try:
        await application.bot.delete_webhook(drop_pending_updates=True)
        webhook_url = f"{WEBHOOK_URL}/webhook"
        await application.bot.set_webhook(url=webhook_url, drop_pending_updates=True)
        logger.info(f"✅ Webhook configurado: {webhook_url}")
    except Exception as e:
        logger.exception("Erro ao configurar webhook")

    yield
    await application.shutdown()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, app.state.application.bot)
        await app.state.application.process_update(update)
        return {"ok": True}
    except Exception as e:
        logger.exception("Erro no webhook")
        return {"ok": False}

@app.get("/")
async def root():
    return {"status": "online", "bot": "OfertaBot IA"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)