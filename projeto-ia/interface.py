import streamlit as st
from src.team import get_team

st.set_page_config(page_title="Atendimento Vértice", layout="centered")

# Estilo para aumentar a caixa de entrada
st.markdown("""
<style>
textarea[data-testid="chat-input"] {
    min-height: 80px !important;
    font-size: 16px !important;
    padding: 12px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("Atendimento Inteligente Vértice")

# Mensagem de boas-vindas
st.markdown("""
Bem-vindo à **Vértice Assessoria de Investimentos**!  
Estamos aqui para te ajudar com suas dúvidas sobre o mercado financeiro, investimentos ou sobre nossa empresa.  
Digite sua pergunta abaixo e nosso time inteligente vai te responder com clareza e simpatia 😊
""")

# estilização
st.markdown("""
<div style="background-color:#f0f8ff; padding:12px; border-left:5px solid #1f77b4; border-radius:6px; margin-bottom:20px;">
<span style="color:#000000;"><strong>Pergunta recomendada:</strong></span><br>
<span style="font-size:15px; color:#000000;">Como os fundos do nosso portfólio estão se relacionando com o desempenho atual do Ibovespa?</span>
</div>
""", unsafe_allow_html=True)

# Inicializa o time
if "team" not in st.session_state:
    st.session_state.team = get_team()

# Inicializa histórico
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Campo de entrada tipo chat
pergunta = st.chat_input("Digite sua pergunta...")

# Processa nova pergunta
if pergunta:
    st.session_state.chat_history.append({"role": "user", "content": pergunta})
    with st.spinner("Pensando na melhor resposta para você..."):
        resposta = st.session_state.team.run(pergunta)
    st.session_state.chat_history.append({"role": "assistant", "content": resposta.content})

# Exibe histórico completo
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"<div style='color:#2c3e50'><strong>🧑 Você:</strong></div><div style='margin-bottom:15px'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='color:#1f77b4'><strong>🤖 Vértice:</strong></div><div style='margin-bottom:15px'>{msg['content']}</div>", unsafe_allow_html=True)
