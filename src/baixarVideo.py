import streamlit as st
from pytube import YouTube
import os
import time

def run():
    st.header("Baixar Vídeo do YouTube", divider=True)
    
    # Campo de entrada para a URL do vídeo
    url = st.text_input("Insira a URL do Vídeo")

    download_option = st.selectbox("Selecione o formato de download:", ["Vídeo", "Áudio"])
        
    # Verifica se a URL é válida
    if url:
        try:
            yt = YouTube(url)

            if yt:
                st.video(url)  # Exibe uma prévia do vídeo
                
                with st.spinner("Processando download..."):
                    # Define o formato de download
                    if download_option == "Vídeo":              
                        video_stream = yt.streams.get_highest_resolution()
                        video_file = video_stream.download()
                        file_name = os.path.basename(video_file)
                        mime_type = "video/mp4"
                    
                    else:
                        video_stream = yt.streams.get_audio_only()
                        video_file = video_stream.download()
                        file_name = os.path.basename(video_file)
                        mime_type = "audio/mp3"

                # Fornece um link para download
                with open(video_file, "rb") as f:
                    st.download_button(
                        label=f"Download do {download_option}",
                        data=f,
                        file_name=file_name,
                        mime=mime_type,
                    )
                    
                st.success(f"{download_option} baixado com sucesso!")
                time.sleep(5)  # Atraso para permitir que o usuário veja a mensagem

                # Remove o arquivo após o download
                if os.path.exists(video_file):
                    os.remove(video_file)

        except Exception as e:
            st.error(f"Erro: {e}")

if __name__ == "__main__":
    run()
