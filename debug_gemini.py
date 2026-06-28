import os
import asyncio
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from telegram.ext import Application

load_dotenv()

app_web = FastAPI()

@app_web.get("/")
async def read_root():
    return {"status": "online", "bot": "OfertaBotIA"}

async def run_web_server():
    port = int(os.getenv("PORT", 10000))
    config = uvicorn.Config(app=app_web, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("❌ BOT_TOKEN não encontrado!")
        return

    print("🚀 Iniciando bot...")

    application = Application.builder().token(token).build()
    await application.initialize()
    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)

    print("🤖 Bot do Telegram rodando!")
    print("🌐 Servidor web iniciando...")

    asyncio.create_task(run_web_server())

    # Loop infinito forte
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())