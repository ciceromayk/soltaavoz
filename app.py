# Importa as bibliotecas necessárias
import streamlit as st
from datetime import datetime
import time # Para simular o tempo de transcrição

# --- Configuração da Página ---
st.set_page_config(
    page_title="Notas de Reunião com Transcrição",
    page_icon="📝",
    layout="centered"
)

# --- Inicialização do Estado da Sessão ---
if "notes" not in st.session_state:
    st.session_state.notes = []

# --- Título e Descrição do Aplicativo ---
st.title("📝 Aplicativo de Notas de Reunião")
st.markdown("Crie notas a partir de texto ou transcreva o áudio de suas reuniões.")
st.markdown("---")

# --- Função de Transcrição (Simulada) ---
def transcribe_audio_dummy(audio_file):
    """
    Função de demonstração que simula uma transcrição de áudio.
    Em um projeto real, esta função seria substituída por uma chamada a uma
    API de reconhecimento de voz.
    """
    # Acessar a API do Google Cloud Speech-to-Text, AWS Transcribe, ou OpenAI Whisper
    # Aqui, retornamos um texto de exemplo para fins de demonstração.
    st.info("Transcrevendo áudio... Isso pode levar alguns segundos.")
    time.sleep(3) # Simula o tempo de processamento da API
    return """
    Olá a todos e bem-vindos à nossa reunião de planejamento do projeto. 
    Hoje, nosso principal objetivo é revisar o progresso da equipe, 
    discutir os próximos passos e atribuir as tarefas para a próxima sprint. 
    Vamos começar com o relatório de status da semana passada.
    """

# --- Seção de Transcrição de Áudio ---
st.subheader("Converter Áudio em Nota")
uploaded_file = st.file_uploader("Escolha um arquivo de áudio (.mp3, .wav, etc.)", type=["mp3", "wav", "ogg"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    if st.button("Transcrever Áudio"):
        with st.spinner("Processando..."):
            transcribed_text = transcribe_audio_dummy(uploaded_file)
        
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
