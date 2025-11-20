from flask import Flask, render_template, request, session, redirect, url_for
import google.generativeai as genai
import json
import os

app = Flask(__name__)
import os
app.secret_key = os.urandom(24)

API_KEY = "AIzaSyDIbZMuVb3k4nxsEJJYNGC3VnuFcEH2OMQ"
genai.configure(api_key=API_KEY)

# Configuração do Modelo
generation_config = {
  "temperature": 0.7,
  "max_output_tokens": 8192,
}
model = genai.GenerativeModel(model_name="gemini-2.5-flash", generation_config=generation_config)

def carregar_adega():
    try:
        with open('vinhos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def analisar_prato_com_ia(prato_usuario):
    prompt = f"""
    Analise o prato: "{prato_usuario}".
    Retorne APENAS um JSON:
    {{ "proteina": "...", "peso": "...", "tags_sugeridas": ["..."] }}
    """
    try:
        response = model.generate_content(prompt)
        texto = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(texto)
    except:
        return None

def filtrar_vinhos(caracteristicas, adega):
    candidatos = []
    if not caracteristicas: return adega
    
    proteina = caracteristicas.get("proteina", "").lower()
    tags_prato = [t.lower() for t in caracteristicas.get("tags_sugeridas", [])]
    
    for vinho in adega:
        pontos = 0
        tipo = vinho["tipo"].lower()
        
        if "carne" in proteina and tipo == "tinto": pontos += 2
        elif "peixe" in proteina and tipo == "branco": pontos += 2
        
        tags_vinho = [t.lower() for t in vinho["tags_harmonizacao"]]
        if set(tags_vinho).intersection(tags_prato):
            pontos += 3
            
        if pontos >= 1:
            candidatos.append(vinho)
            
    return candidatos if candidatos else adega

def gerar_recomendacao_html(prato, lista_vinhos):
    lista_texto = json.dumps(lista_vinhos, ensure_ascii=False)
    prompt = f"""
    Atue como um Sommelier. O cliente vai comer: "{prato}".
    Vinhos disponíveis: {lista_texto}
    
    Escreva um texto curto (bastante resumido e direto), elegante e persuasivo recomendando o melhor vinho.
    Use tags HTML para formatar: use <h3> para o nome do vinho, <p> para o texto e <strong> para destaque.
    Não use Markdown, use apenas HTML.
    """
    response = model.generate_content(prompt)
    return response.text

def registrar_historico(prato, recomendacao):
    if "historico" not in session:
        session["historico"] = []
    session["historico"].append({
        "prato": prato,
        "recomendacao": recomendacao
    })
    session.modified = True


@app.route('/', methods=['GET', 'POST'])
def index():
    recomendacao = ""
    prato_digitado = ""

    if request.method == 'POST':
        prato_digitado = request.form.get('prato')
        adega = carregar_adega()

        # 1. IA Analisa
        caracteristicas = analisar_prato_com_ia(prato_digitado)
        # 2. Filtra
        vinhos = filtrar_vinhos(caracteristicas, adega)
        # 3. Recomenda
        recomendacao = gerar_recomendacao_html(prato_digitado, vinhos)

        # 4. Salvar no histórico
        registrar_historico(prato_digitado, recomendacao)

    return render_template('index.html', recomendacao=recomendacao, prato=prato_digitado)

@app.route('/historico')
def ver_historico():
    historico = session.get("historico", [])
    return render_template('historico.html', historico=historico)

@app.route('/limpar_historico')
def limpar_historico():
    session.pop("historico", None)
    return redirect(url_for('ver_historico'))


if __name__ == '__main__':
    app.run(debug=True)