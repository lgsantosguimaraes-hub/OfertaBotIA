import logging
import csv
import os
import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from app.services.shopee import gerar_link_afiliado

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **OfertaBot IA Ativo!**\n\n"
        "Comandos:\n"
        "/carregar - Enviar ofertas\n"
        "/adicionar Nome https://link - Adicionar nova oferta"
    )

async def carregar_ofertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    csv_path = "produtos.csv"
    if not os.path.exists(csv_path):
        await update.message.reply_text("❌ produtos.csv não encontrado.")
        return

    try:
        count = 0
        await update.message.reply_text("⏳ Enviando ofertas do CSV...")

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                nome = row.get('Offer Name', row.get('nome', 'Produto')).strip()
                link = row.get('Offer Link', row.get('link', '')).strip()
                preco = row.get('preco', '').strip()

                if not link or not nome:
                    continue

                link_afiliado = gerar_link_afiliado(link)

                texto = f"🔥 **{nome}**"
                if preco:
                    texto += f"\n💰 R$ {preco}"
                texto += f"\n\n{link_afiliado}\n\n🛒 Aproveite!"

                await update.message.reply_text(texto)
                count += 1
                await asyncio.sleep(12)  # delay entre posts

        await update.message.reply_text(f"✅ {count} ofertas enviadas com sucesso!")
    except Exception as e:
        logger.error(f"Erro no carregar: {e}")
        await update.message.reply_text("❌ Erro ao processar CSV.")

async def adicionar_oferta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("❌ Uso: /adicionar Nome https://link")
            return

        nome = " ".join(args[:-1])
        link = args[-1]

        with open("produtos.csv", "a", encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([nome, link, "", ""])

        await update.message.reply_text(f"✅ Oferta adicionada!\n**{nome}**")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("❌ Erro ao adicionar oferta.")