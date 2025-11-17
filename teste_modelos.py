import google.generativeai as genai

API_KEY = "AIzaSyDIbZMuVb3k4nxsEJJYNGC3VnuFcEH2OMQ"
genai.configure(api_key=API_KEY)

print("🔍 Buscando modelos disponíveis para sua chave...")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Erro ao listar: {e}")