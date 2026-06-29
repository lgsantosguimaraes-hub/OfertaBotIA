# app/bot/handlers.py
import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Bem-vindo ao OfertaBot IA\n\n"
        "Use /meuid para testar o ID do chat.\n"
        "Em breve mais comandos e ofertas automáticas."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponíveis:\n"
        "/start - Iniciar o bot\n"
        "/meuid - Ver ID do chat"
    )