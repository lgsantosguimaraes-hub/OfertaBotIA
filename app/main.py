import os
import logging
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from telegram import Update
from telegram.ext import Application, CommandHandler

load_dotenv()

# =====================================================
# CONFIG
# =====================================================

TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://ofertabotia.onrender.com").strip()

if not TOKEN:
    raise RuntimeError("❌ TELEGRAM_TOKEN não encontrado no .env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

# =====================================================
# LIFESPAN
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 60)
    logger.info("🚀 INICIANDO OFERTABOT IA")
    logger.info("=" * 60)

    # Cria Application
    application = Application.builder().token(TOKEN).updater(None).build()
    app.state.application = application   # Salva para usar no webhook

    await application.initialize()

    # Configura Webhook
    try:
        await application.bot.delete_webhook(drop_pending_updates=True)

        webhook_url = f"{WEBHOOK_URL}/webhook"
        await application.bot.set_webhook(
            url=webhook_url,
            drop_pending_updates=True
        )

        info = await application.bot.get_webhook_info()
        logger.info(f"✅ Webhook configurado: {info.url}")
        logger.info(f"Pending updates: {info.pending_update_count}")
    except Exception as e:
        logger.exception("❌ Erro ao configurar webhook")

    # Registra handlers
    application.add_handler(CommandHandler("meuid", pegar_id))

    yield

    logger.info("⛔ Encerrando OfertaBot IA...")
    await application.shutdown()

# =====================================================
# APP
# =====================================================

app = FastAPI(lifespan=lifespan, title="OfertaBot IA")

# =====================================================
# HANDLER
# =====================================================

async def pegar_id(update: Update, context):
    chat_id = update.effective_chat.id
    logger.info(f"ID capturado: {chat_id}")
    await update.message.reply_text(
        f"O ID deste chat é:\n\n`{chat_id}`",
        parse_mode="MarkdownV2"
    )

# =====================================================
# WEBHOOK
# =====================================================

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, app.state.application.bot)
        await app.state.application.process_update(update)
        return {"ok": True}
    except Exception as e:
        logger.exception("Erro ao processar update")
        return {"ok": False}

# =====================================================
# HEALTH
# =====================================================

@app.get("/")
async def root():
    return {
        "status": "online",
        "bot": "OfertaBot IA",
        "webhook": f"{WEBHOOK_URL}/webhook"
    }

# =====================================================
# START
# =====================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)