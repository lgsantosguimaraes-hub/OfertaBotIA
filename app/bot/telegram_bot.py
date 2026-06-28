import os
import asyncio
import uvicorn
from fastapi import FastAPI
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

app_web = FastAPI()

@app_web.get("/")
async def read_root():
    return {"status": "online"}

async def run_web_server():
    port = int(os.getenv("PORT", 10000))
    config = uvicorn.Config(
        app=app_web,
        host="0.0.0.0",
        port=port,
        log_level="info",
        timeout_keep_alive=65,
    )
    server = uvicorn.Server(config)
    await server.serve()

# --- COMANDO PARA DESCOBRIR ID ---
async def pegar_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Envia o ID para o chat atual (pode ser privado ou canal)
    await update.message.reply_text(f"O ID deste chat é: {update.effective_chat.id}")

async def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("❌ ERRO: Variável TELEGRAM_TOKEN não encontrada!")
        return

    # === CONFIGURAÇÃO DO BOT ===
    # drop_pending_updates=True limpa mensagens antigas que causavam o erro de conflito
    application = Application.builder().token(token).build()
    
    # Handlers
    application.add_handler(CommandHandler("meuid", pegar_id))
    
    # Inicialização correta
    await application.initialize()
    await application.start()
    
    # Inicia o polling com limpeza de conflitos
    print("🚀 Iniciando polling do bot...")
    await application.updater.start_polling(drop_pending_updates=True)

    # === INICIA O SERVIDOR WEB EM BACKGROUND ===
    web_task = asyncio.create_task(run_web_server())
    
    print(f"✅ Servidor web iniciado na porta {os.getenv('PORT', 10000)}")
    print("🤖 Bot está rodando...")
    
    # Mantém o programa rodando
    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        pass
    finally:
        # Shutdown gracioso para evitar conflitos futuros
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
        web_task.cancel()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass