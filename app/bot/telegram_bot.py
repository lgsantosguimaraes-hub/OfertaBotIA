import asyncio
from aiohttp import web
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from app.services.llm_service import LLMService

# --- CONFIGURAÇÃO ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

TOKEN = os.getenv("BOT_TOKEN")
llm_service = LLMService()

# --- SERVIDOR WEB (PARA O RENDER) ---
async def start_web_server():
    app = web.Application()
    app.router.add_get('/', lambda r: web.Response(text="Bot is running!"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    print("🌐 Servidor web rodando na porta 10000")

# --- FUNÇÕES DO BOT ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **OfertaBot IA ativo!**\n\n"
        "Me envie o link de um produto e eu cuidarei da copy para você!"
    )

async def postar_oferta_agendada(context: ContextTypes.DEFAULT_TYPE):
    link, contexto = context.job.data
    copy = await llm_service.gerar_copy_venda(link, contexto)
    await context.bot.send_message(chat_id=context.job.chat_id, text=copy)

async def agendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /agendar [segundos] [link] [contexto...]")
        return
    segundos = int(context.args[0])
    link = context.args[1]
    contexto = " ".join(context.args[2:])
    context.job_queue.run_once(postar_oferta_agendada, segundos, chat_id=update.effective_chat.id, data=(link, contexto))
    await update.message.reply_text(f"✅ Agendado para daqui a {segundos}s.")

async def processar_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    if not texto: return
    
    links = re.findall(r'(https?://(?:[a-zA-Z0-9\.]+)?shopee\.com\.br/[^\s]+|https?://shp\.ee/[^\s]+)', texto)
    if links:
        link = links[0].rstrip('.,;)[]')
        msg = await update.message.reply_text("🤖 Gerando copy...")
        contexto = texto.replace(link, "").strip()
        copy = await llm_service.gerar_copy_venda(link, contexto if contexto else None)
        await msg.delete()
        await update.message.reply_text(copy)

# --- INICIALIZAÇÃO ---

async def main():
    print("🤖 Iniciando o OfertaBot IA...")
    
    # 1. Inicia o servidor web em paralelo
    await start_web_server()
    
    # 2. Configura o bot
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("agendar", agendar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_texto))
    
    print("✅ Bot rodando! Pressione Ctrl+C para parar.")
    
    # 3. Inicia o polling do Telegram
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())