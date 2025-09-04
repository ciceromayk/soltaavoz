# Importa as bibliotecas necessárias
import streamlit as st
from datetime import datetime
import openai # A biblioteca da OpenAI
import os # Para gerenciar variáveis de ambiente e chaves de API

# --- Configuração da Página ---
st.set_page_config(
    page_title="Notas de Reunião com Transcrição Real",
    page_icon="📝",
    layout="centered"
)

# --- Inicialização do Estado da Sessão ---
if "notes" not in st.session_state:
    st.session_state.notes = []

# --- Configuração da API da OpenAI ---
# É mais seguro armazenar a chave de API em variáveis de ambiente.
# Substitua 'SUA_CHAVE_DE_API_DA_OPENAI' pela sua chave.
openai.api_key = os.getenv("OPENAI_API_KEY", "SUA_CHAVE_DE_API_DA_OPENAI")

# --- Função de Transcrição Real com a API da OpenAI (Whisper) ---
def transcribe_audio(audio_file):
    """
    Função que usa a API da OpenAI para transcrever um arquivo de áudio.
    """
    try:
        # Abre o arquivo de áudio para a API
        with open("uploaded_audio.mp3", "wb") as f:
            f.write(audio_file.getbuffer())
        
        # Chama a API de áudio da OpenAI
        with open("uploaded_audio.mp3", "rb") as audio:
            transcription = openai.Audio.transcribe("whisper-1", audio)
        
        return transcription.text
    except Exception as e:
        st.error(f"Erro ao transcrever o áudio: {e}")
        return None

# --- Título e Descrição do Aplicativo ---
st.title("📝 Aplicativo de Notas de Reunião")
st.markdown("Crie notas a partir de texto ou transcreva o áudio de suas reuniões.")
st.markdown("---")

# --- Seção de Transcrição de Áudio ---
st.subheader("Converter Áudio em Nota")
uploaded_file = st.file_uploader("Escolha um arquivo de áudio (.mp3, .wav, etc.)", type=["mp3", "wav", "ogg"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    
    if st.button("Transcrever Áudio"):
        with st.spinner("Transcrevendo áudio... Isso pode levar alguns segundos."):
            transcribed_text = transcribe_audio(uploaded_file)
        
        if transcribed_text:
            st.success("Transcrição concluída com sucesso!")
            
            # Cria um formulário para o usuário editar e salvar a nota transcrita
            with st.form(key="transcription_form"):
                st.markdown("### Transcrição da Reunião")
                title = st.text_input("Título da Nota", value=f"Reunião em {datetime.now().strftime('%d/%m/%Y')}")
                content = st.text_area("Texto Transcrito", value=transcribed_text, height=250)
                
                save_button = st.form_submit_button("Salvar Nota Transcrita")
                
                if save_button and title and content:
                    new_note = {
                        "title": title,
                        "content": content,
                        "timestamp": datetime.now().strftime("%d/%m/%Y às %H:%M")
                    }
                    st.session_state.notes.append(new_note)
                    st.toast("Nota salva com sucesso!", icon="✅")
        
# --- Formulário para Adicionar Nota Manualmente ---
st.markdown("---")
st.subheader("Adicionar Nova Nota Manualmente")
with st.form(key="note_form", clear_on_submit=True):
    title = st.text_input("Título da Reunião", placeholder="Ex: Reunião de brainstorming")
    content = st.text_area("Notas da Reunião", placeholder="O que foi discutido...")
    
    submit_button = st.form_submit_button("Salvar Nota")

    if submit_button and title and content:
        new_note = {
            "title": title,
            "content": content,
            "timestamp": datetime.now().strftime("%d/%m/%Y às %H:%M")
        }
        st.session_state.notes.append(new_note)
        st.toast("Nota salva com sucesso!", icon="✅")

# --- Exibição das Notas Salvas ---
st.markdown("---")
st.subheader("Minhas Notas")

if not st.session_state.notes:
    st.info("Nenhuma nota salva ainda. Use um dos formulários acima para adicionar uma nota.")
else:
    reversed_notes = st.session_state.notes[::-1]
    
    for i, note in enumerate(reversed_notes):
        with st.expander(f"**{note['title']}** - *{note['timestamp']}*"):
            st.write(f"Conteúdo:\n\n{note['content']}")
            
            # Botão de apagar a nota
            if st.button("Apagar", key=f"delete_button_{i}"):
                original_index = len(st.session_state.notes) - 1 - i
                st.session_state.notes.pop(original_index)
                st.rerun()
    
    st.markdown("---")
    if st.button("Apagar Todas as Notas", key="clear_all"):
        st.session_state.notes = []
        st.toast("Todas as notas foram apagadas.", icon="🗑️")
        st.rerun()
