import asyncio
import os
import re
import uvicorn
from fastapi import FastAPI
from threading import Thread
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from app.services.llm_service import LLMService

# ... (seus outros imports e configurações)

# --- SERVIDOR FASTAPI (MAIS COMPATÍVEL COM RENDER) ---
app_web = FastAPI()

@app_web.get("/")
def read_root():
    return {"status": "online"}

def run_server():
    # O Render injeta a porta na variável de ambiente PORT, ou usamos 10000
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app_web, host="0.0.0.0", port=port)

# --- INICIALIZAÇÃO ---

async def main():
    # 1. Inicia o servidor web em uma thread separada (não bloqueante)
    Thread(target=run_server, daemon=True).start()
    print("🌐 Servidor web iniciado pelo Uvicorn")

    # 2. Configura o bot
    app = Application.builder().token(TOKEN).build()
    # ... (seus handlers: add_handler...)
    
    print("✅ Bot rodando!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())