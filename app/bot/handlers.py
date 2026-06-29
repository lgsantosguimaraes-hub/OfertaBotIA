import logging
import csv
import os
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 **OfertaBot IA Ativo!**\nUse /carregar para ofertas.")

async def carregar_ofertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    csv_path = "produtos.csv"
    
    if not os.path.exists(csv_path):
        await update.message.reply_text("❌ Arquivo produtos.csv não encontrado.")
        return

    try:
        count = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                nome = row.get('Offer Name', row.get('nome', 'Produto')).strip()
                link = row.get('Offer Link', row.get('link', '')).strip()
                if link and nome:
                    await update.message.reply_text(f"🔥 **{nome}**\n{link}")
                    count += 1
                if count >= 10:
                    break

        await update.message.reply_text(f"✅ {count} ofertas enviadas com sucesso!")
        logger.info(f"Carregadas {count} ofertas.")
    except Exception as e:
        logger.error(f"Erro no carregar: {e}")
        await update.message.reply_text(f"❌ Erro ao ler CSV: {str(e)[:100]}")