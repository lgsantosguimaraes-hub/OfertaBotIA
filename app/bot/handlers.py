import logging
import csv
import os
import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from app.services.shopee import gerar_link_afiliado
from app.services.shopee_api import ShopeeAPI
from app.utils.cache import is_product_sent, mark_product_sent

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **OfertaBot IA Ativo!**\n\n"
        "Comandos:\n"
        "/carregar - Buscar novas ofertas\n"
        "/adicionar Nome https://link - Adicionar manual"
    )

async def carregar_ofertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Buscando ofertas novas na Shopee...")

    shopee = ShopeeAPI()
    products = await shopee.get_products(limit=15)

    if not products:
        await update.message.reply_text("❌ Nenhuma oferta nova encontrada.")
        return

    count = 0
    for product in products:
        item_id = str(product.get('item_id'))
        nome = product.get('name', 'Produto')
        link = product.get('url', '')
        preco = product.get('price', 0)

        if not link or is_product_sent(item_id):
            continue

        link_afiliado = gerar_link_afiliado(link)

        texto = f"🔥 **{nome}**\n💰 R$ {preco:,}\n\n{link_afiliado}\n\n🛒 Aproveite!"

        await update.message.reply_text(texto)
        mark_product_sent(item_id)

        count += 1
        await asyncio.sleep(12)  # ~12 segundos entre posts

    await update.message.reply_text(f"✅ {count} **novas** ofertas enviadas!")