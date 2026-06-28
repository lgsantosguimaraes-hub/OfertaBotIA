import os
import re
import csv
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from app.services.llm_service import LLMService

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

TOKEN = os.getenv("BOT_TOKEN")
llm_service = LLMService()

# --- FUNÇÕES ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 **OfertaBot IA ativo!**\nEnvie links ou use /carregar para processar sua lista CSV.")

async def postar_oferta_agendada(context: ContextTypes.DEFAULT_TYPE):
    link, nome = context.job.data
    # Usamos o nome como contexto para a IA gerar uma copy melhor
    copy = await llm_service.gerar_copy_venda(link, contextualizacao=nome)
    await context.bot.send_message(chat_id=context.job.chat_id, text=copy)

async def carregar_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lê o arquivo produtos.csv da raiz, verifica validade e agenda tudo"""
    try:
        caminho_arquivo = BASE_DIR / "produtos.csv"
        hoje = datetime.now()
        agendamento = 0
        intervalo = 300 # 5 minutos
        avisos = []
        
        with open(caminho_arquivo, mode='r', encoding='utf-8') as f:
            leitor = csv.DictReader(f)
            for linha in leitor:
                # Extração de data e limpeza de nome
                periodo_str = linha['Offer Period']
                data_fim_str = periodo_str.split("end: ")[1].split("\n")[0].strip()
                data_fim = datetime.strptime(data_fim_str, "%Y-%m-%d")
                
                dias_restantes = (data_fim - hoje).days
                nome = linha['Offer Name'].replace("- - ", "").strip()
                
                # Alerta se expira em breve
                if dias_restantes <= 3:
                    avisos.append(f"⚠️ {nome} (Expira em {dias_restantes} dias)")
                
                # Agendamento
                context.job_queue.run_once(
                    postar_oferta_agendada, 
                    agendamento, 
                    chat_id=update.effective_chat.id, 
                    data=(linha['Offer Link'], nome)
                )
                agendamento += intervalo
        
        if avisos:
            await update.message.reply_text("🚨 **Atenção - Ofertas vencendo:**\n" + "\n".join(avisos))
        await update.message.reply_text(f"✅ Lista carregada! Ofertas agendadas com sucesso.")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao processar arquivo: {e}")

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

def main():
    print("🤖 Iniciando o OfertaBot IA com agendador...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("carregar", carregar_lista))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_texto))
    
    print("✅ Bot pronto! Pressione Ctrl+C para parar.")
    app.run_polling()

if __name__ == "__main__":
    main()