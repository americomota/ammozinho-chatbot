import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# -----------------------------
# 🔐 Carregar chave da OpenAI
# -----------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ A chave da API da OpenAI não foi encontrada no arquivo .env.")
    st.stop()

client = OpenAI(api_key=api_key)

# -----------------------------
# 📄 Função para carregar arquivos .txt
# -----------------------------
def carregar_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"❌ Arquivo '{nome_arquivo}' não encontrado.")
        st.stop()

# -----------------------------
# 📚 Carregar instruções e contexto
# -----------------------------
comportamento_do_bot = carregar_arquivo("instrucoes_bot.txt")
contexto = carregar_arquivo("contexto.txt")

# -----------------------------
# 🤖 Função para perguntar à OpenAI
# -----------------------------
def perguntar_openai(pergunta):
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": comportamento_do_bot},
            {"role": "user", "content": f"Base de conhecimento:\n{contexto}"},
            {"role": "user", "content": pergunta}
        ],
        max_tokens=1000,
        temperature=0
    )
    return resposta.choices[0].message.content

# -----------------------------
# 🌐 INTERFACE STREAMLIT
# -----------------------------
st.set_page_config(page_title="Ammozinho - Assistente AI", page_icon="🤖")
st.title("🤖 Ammozinho - Agente IA da Pós em Ultrassom do Instituto AMMO")
st.markdown("Olá! Eu sou o **Ammozinho**, Agente de IA da Pós de Ultrassom do Instituto AMMO. Como posso te ajudar hoje?")

# Histórico da conversa
if "historico" not in st.session_state:
    st.session_state.historico = []

# Formulário de entrada
with st.form(key="formulario_pergunta"):
    pergunta = st.text_input("Digite sua pergunta:")
    enviar = st.form_submit_button("Enviar")

if enviar and pergunta:
    st.session_state.historico.append(("Você", pergunta))
    resposta = perguntar_openai(pergunta)
    st.session_state.historico.append(("Ammozinho", resposta))
    st.rerun()

# Exibir conversa
for autor, mensagem in st.session_state.historico:
    st.markdown(f"**{autor}:** {mensagem}")

# Botão para limpar a conversa
if st.button("🧹 Limpar conversa"):
    st.session_state.historico = []
    st.rerun()

# Rodapé
st.markdown("---")
st.caption("Desenvolvido por Américo Mota - AMMO ❤️")
