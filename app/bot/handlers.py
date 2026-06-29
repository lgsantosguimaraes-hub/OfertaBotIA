import logging
import csv
import os
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 **OfertaBot IA Ativo!**\nUse /carregar")

async def carregar_ofertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    csv_path = "produtos.csv"
    if not os.path.exists(csv_path):
        await update.message.reply_text("❌ produtos.csv não encontrado.")
        return

    try:
        count = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                nome = row.get('Offer Name', row.get('nome', 'Produto')).strip()
                link = row.get('Offer Link', row.get('link', '')).strip()
                preco = row.get('preco', '').strip()
                imagem = row.get('imagem', '').strip()

                texto = f"🔥 **{nome}**"
                if preco:
                    texto += f"\n💰 R$ {preco}"
                texto += f"\n\n{link}\n\n🛒 Aproveite!"

                if imagem and imagem.startswith("http"):
                    await update.message.reply_photo(photo=imagem, caption=texto)
                else:
                    await update.message.reply_text(texto)

                count += 1
                if count >= 8:
                    break

        await update.message.reply_text(f"✅ {count} ofertas enviadas!")
    except Exception as e:
        logger.error(f"Erro: {e}")
        await update.message.reply_text("❌ Erro ao processar.")