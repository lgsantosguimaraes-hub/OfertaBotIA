import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega as variáveis do seu arquivo .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("=== DIAGNÓSTICO DO GEMINI ===")

if not api_key:
    print("❌ ERRO: Nenhuma chave encontrada na variável GEMINI_API_KEY do .env")
else:
    print(f"✅ Chave identificada: {api_key[:5]}...{api_key[-5:]}")
    
    genai.configure(api_key=api_key)
    
    try:
        print("🔍 Perguntando ao Google quais modelos estão liberados para esta chave...")
        modelos_encontrados = False
        
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f" 🟢 Modelo disponível: {m.name}")
                modelos_encontrados = True
                
        if not modelos_encontrados:
            print("⚠️ A chave é válida, mas a sua conta não tem NENHUM modelo de texto liberado.")
            
    except Exception as e:
        print(f"\n❌ Falha grave de comunicação com o Google:\n{e}")
        
print("=============================")