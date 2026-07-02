import logging
import csv
import os
import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from app.services.shopee import gerar_link_afiliado
from app.services.shopee_api import ShopeeAPI

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **OfertaBot IA Ativo!**\n\n"
        "Comandos:\n"
        "/carregar - Buscar ofertas bonitas\n"
        "/adicionar Nome https://link - Adicionar manual"
    )

async def carregar_ofertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Buscando ofertas na Shopee...")

    shopee = ShopeeAPI()
    products = await shopee.get_products(limit=8)

    if not products:
        await update.message.reply_text("❌ Nenhuma oferta encontrada no momento.")
        return

    count = 0
    for product in products:
        nome = product.get('productName', 'Produto Shopee')
        link = product.get('offerLink', product.get('productLink', ''))
        preco = product.get('price', 0)
        original = product.get('originalPrice', 0)
        imagem = product.get('image', '')
        desconto = product.get('discount', '')

        if not link:
            continue

        link_afiliado = gerar_link_afiliado(link)

        # Monta legenda bonita
        legenda = f"🔥 **{nome}**\n\n"
        if original and original > preco:
            legenda += f"💰 De: R$ {original:,}\n"
            legenda += f"💸 Por: R$ {preco:,}\n"
        else:
            legenda += f"💰 R$ {preco:,}\n"
        
        if desconto:
            legenda += f"🔥 {desconto}% OFF\n"
        
        legenda += f"\n{link_afiliado}\n\n"
        legenda += "🛒 Aproveite! Entrega rápida."

        try:
            if imagem and imagem.startswith("http"):
                await update.message.reply_photo(photo=imagem, caption=legenda)
            else:
                await update.message.reply_text(legenda)
        except:
            await update.message.reply_text(legenda)

        count += 1
        await asyncio.sleep(15)  # delay entre posts

    await update.message.reply_text(f"✅ {count} ofertas bonitas enviadas!")