# app/services/llm_service.py
import os
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class LLMService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
            self.model_name = 'gemini-2.5-flash'
        else:
            self.client = None

    async def gerar_copy_venda(self, link_produto: str, contextualizacao: str = None) -> str:
        termo_produto = contextualizacao if contextualizacao else "Oferta"
        
        prompt = (
            f"Você é um bot de ofertas. Produto: {termo_produto}. Link: {link_produto}.\n"
            f"Siga este padrão:\n[Nome em negrito]\n[Link]\n💰 [Preço se houver]\n🏷️ [Cupom se houver]\n"
            f"Seja objetivo, máximo 5 linhas."
        )

        try:
            # Nova sintaxe da biblioteca google.genai
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return response.text
        except Exception:
            return f"🛒 **{termo_produto}**\n👉 {link_produto}"