import os
import logging

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler

load_dotenv()

# =====================================================
# LOGS
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# =====================================================
# CONFIG
# =====================================================

TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://ofertabotia.onrender.com").strip()

if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN não encontrado.")

app = FastAPI()

# =====================================================
# APPLICATION (SEM POLLING)
# =====================================================

application = (
    Application.builder()
    .token(TOKEN)
    .updater(None)
    .build()
)

# =====================================================
# COMANDOS
# =====================================================

async def pegar_id(update: Update, context):
    chat_id = update.effective_chat.id

    logger.info(f"ID capturado: {chat_id}")

    await update.message.reply_text(
        f"O ID deste chat é:\n\n{chat_id}"
    )

application.add_handler(CommandHandler("meuid", pegar_id))

# =====================================================
# STARTUP
# =====================================================

@app.on_event("startup")
async def startup():

    logger.info("=" * 60)
    logger.info("Inicializando OfertaBotIA")
    logger.info("=" * 60)

    await application.initialize()

    logger.info("Application inicializada.")

    try:

        logger.info("Removendo webhook antigo...")

        await application.bot.delete_webhook(
            drop_pending_updates=True
        )

        logger.info("Webhook antigo removido.")

        logger.info("Criando novo webhook...")

        ok = await application.bot.set_webhook(
            url=f"{WEBHOOK_URL}/webhook",
            drop_pending_updates=True,
        )

        logger.info(f"Webhook criado: {ok}")

        info = await application.bot.get_webhook_info()

        logger.info("========== WEBHOOK INFO ==========")
        logger.info(f"URL: {info.url}")
        logger.info(f"Pending: {info.pending_update_count}")
        logger.info(f"Último erro: {info.last_error_message}")
        logger.info(f"Max Connections: {info.max_connections}")
        logger.info("=================================")

    except Exception as e:
        logger.exception("Erro ao configurar webhook.")

# =====================================================
# SHUTDOWN
# =====================================================

@app.on_event("shutdown")
async def shutdown():

    logger.info("Finalizando aplicação...")

    await application.shutdown()

# =====================================================
# WEBHOOK
# =====================================================

@app.post("/webhook")
async def webhook(request: Request):

    try:

        data = await request.json()

        logger.info(f"Update recebido: {data}")

        update = Update.de_json(data, application.bot)

        await application.process_update(update)

    except Exception:
        logger.exception("Erro ao processar update.")

    return {"ok": True}

# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/")
async def root():

    return {
        "status": "online",
        "bot": "OfertaBotIA",
    }

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    port = int(os.getenv("PORT", 10000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )