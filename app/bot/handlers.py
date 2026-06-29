import logging
import csv
import os
from telegram import Update
from telegram.ext import ContextTypes

from app.services.shopee import gerar_link_afiliado

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **OfertaBot IA Ativo!**\n\n"
        "Use /carregar para processar as ofertas."
    )

async def carregar_ofertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    csv_path = "produtos.csv"
    
    if not os.path.exists(csv_path):
        await update.message.reply_text("❌ Arquivo `produtos.csv` não encontrado na raiz.")
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

                if not link or not nome:
                    continue

                # Gera link de afiliado
                link_afiliado = gerar_link_afiliado(link)

                texto = f"🔥 **{nome}**"
                if preco:
                    texto += f"\n💰 R$ {preco}"
                texto += f"\n\n{link_afiliado}\n\n🛒 Aproveite esta oferta!"

                try:
                    if imagem and imagem.startswith("http"):
                        await update.message.reply_photo(photo=imagem, caption=texto)
                    else:
                        await update.message.reply_text(texto)
                except Exception:
                    await update.message.reply_text(texto)  # fallback sem imagem

                count += 1
                if count >= 10:  # limite de segurança
                    break

        await update.message.reply_text(f"✅ {count} ofertas enviadas com sucesso!")
        logger.info(f"Processadas {count} ofertas.")
    except Exception as e:
        logger.error(f"Erro no /carregar: {e}")
        await update.message.reply_text("❌ Erro ao processar as ofertas.")