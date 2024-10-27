import streamlit as st
from pytube import YouTube
import os
from pytubefix import YouTube
from pytubefix.cli import on_progress
import time

def run():
    st.header("Baixar Vídeo do YouTube", divider=True)
    verifica=''
    # Campo de entrada para a URL do vídeo
    url = st.text_input("Insira a URL do Vídeo")

    download_option = st.selectbox("Selecione o formato de download:", ["Vídeo", "Áudio"])
        
    # Verifica se a URL é válida
    if url and url != "Cole aqui a URL":
        
        try:
            yt = YouTube(url)

            st.video(url)  # Exibe uma prévia do vídeo com tamanho reduzido
            
            st.spinner("Em processamento...")
            # Botão para download
            if yt:
                # Faz o download do vídeo na melhor resolução

                if download_option=="Vídeo":              
                    video_stream = yt.streams.get_highest_resolution(progressive=True)
                    video_file = video_stream.download()  # Faz o download
                    file_name = os.path.basename(video_file)
                    mime_type = "video/mp4"
                
                else:
                    video_stream = yt.streams.get_audio_only()
                    video_file = video_stream.download()  # Faz o download
                    file_name = os.path.basename(video_file)
                    mime_type = "audio/mp3"

                
                # Fornece um link para download
                with open(video_file, "rb") as f:
                  
                    if st.download_button(
                        label=f"Download do {download_option}",
                        data=f,
                        file_name=file_name,
                        mime=mime_type,
                    ):
                        if download_option:
                            st.spinner(f"Baixando {download_option}...")
                            st.success(f"{download_option} baixado com Sucesso")
                        f.close()
                        
                        time.sleep(5)
                        if os.path.exists(video_file):
                            os.remove(video_file)
                    else:
                        f.close()
                        os.remove(video_file)

                        
                    
                #
                #         
                    
                        
                    
        except Exception as e:
            st.error(f"Erro: {e}")

if __name__ == "__main__":
    run()
