# Sistema de recomendação de vinhos

## Como funciona?

Nosso sistema de recomendação leva em conta alguns pontos acerca dos pratos escolhidos pelos usuários para fazer uma sugestão acertiva que combine perfeitamente.

## Instalação e execução (fluxo recomendado)

1) Clonar o repositório:

```bash
git clone <url do repositório>
```

2) Criar e ativar um ambiente virtual (recomendado para não gerar conflitos):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3) Instalar dependências:

```bash
pip install flask streamlit google-generativeai
```

4) Executar a aplicação:

# Rodar a app Flask (padrão do projeto):
```bash
python app.py
```

# Rodar a interface Streamlit (se for usá-la):
```bash
streamlit run site_vinhos.py
```








