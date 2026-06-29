# app/bot/webhook.py
import logging
from fastapi import Request
from telegram import Update
from telegram.ext import Application

from app.bot.telegram_bot import bot, dp, TOKEN

logger = logging.getLogger(__name__)

async def set_webhook():
    """Configura o webhook do Telegram"""
    webhook_url = "https://seu-app.onrender.com/webhook"  # ← vai ser atualizado via .env
    await bot.set_webhook(webhook_url)
    logger.info(f"Webhook configurado: {webhook_url}")

# Webhook endpoint para o FastAPI
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, bot)
        await dp.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Erro no webhook: {e}")
        return {"status": "error"}