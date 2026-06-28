from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="OfertaBot IA")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>OfertaBot IA</title>
        </head>
        <body style="font-family:Arial;text-align:center;margin-top:80px;">
            <h1>🚀 OfertaBot IA</h1>
            <h2>Projeto iniciado com sucesso!</h2>
            <p>Em breve você poderá publicar ofertas automaticamente no Telegram.</p>
        </body>
    </html>
    """