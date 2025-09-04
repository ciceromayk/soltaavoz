# Importa as bibliotecas necessárias
import streamlit as st
from datetime import datetime
from google.cloud import speech # A biblioteca do Google Cloud
import os
import io

# --- Configuração da Página ---
st.set_page_config(
    page_title="Notas de Reunião com Transcrição Real",
    page_icon="📝",
    layout="centered"
)

# --- Inicialização do Estado da Sessão ---
if "notes" not in st.session_state:
    st.session_state.notes = []

# --- Configuração da API do Google Cloud ---
# Para autenticação, você deve definir a variável de ambiente
# GOOGLE_APPLICATION_CREDENTIALS que aponta para o seu arquivo JSON de credenciais.
# Exemplo de como fazer no terminal:
# export GOOGLE_APPLICATION_CREDENTIALS="/caminho/para/seu/arquivo.json"
# Ou, para fins de teste, você pode carregar o JSON diretamente (não recomendado para produção).

# --- Função de Transcrição Real com a API do Google Cloud ---
def transcribe_audio_google(audio_file):
    """
    Função que usa a API do Google Cloud para transcrever um arquivo de áudio.
    """
    try:
        # Instancia o cliente da API
        client = speech.SpeechClient()
        
        # Lê o arquivo de áudio e o prepara para a API
        audio_bytes = audio_file.read()
        audio = speech.RecognitionAudio(content=audio_bytes)
        
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS, # ou MP3, WAV
            sample_rate_hertz=48000, # Ajuste conforme seu arquivo
            language_code="pt-BR", # Idioma do áudio
        )
        
        with st.spinner("Transcrevendo áudio... Isso pode levar algum tempo."):
            response = client.recognize(config=config, audio=audio)
        
        # Concatena os resultados da transcrição
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + " "
        
        return transcript
    except Exception as e:
        st.error(f"Erro ao transcrever o áudio: {e}")
        st.info("Verifique se a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS está configurada corretamente.")
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
        transcribed_text = transcribe_audio_google(uploaded_file)
        
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
