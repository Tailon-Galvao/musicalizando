import streamlit as st
import numpy as np
from st_on_hover_tabs import on_hover_tabs
import importlib
import os

# Definindo o caminho do arquivo CSS
css_file_path = os.path.join(os.path.dirname(__file__), '../css/style.css')
# css_file_path = '../css/style.css'

# Configurações da página
st.set_page_config(page_title="Musicalizando", layout="wide")

# Aplicar estilo CSS personalizado
# st.markdown('<style>' + open(css_file_path).read() + '</style>', unsafe_allow_html=True)

# Aplicar estilo CSS personalizado
try:
    with open(css_file_path) as f:
        st.markdown('<style>' + f.read() + '</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"Arquivo CSS não encontrado: {css_file_path}")

# Sidebar com imagem e tabs de navegação
image_path='../img/music.png'
with st.sidebar:
   try:
        st.image(
            image_path,
            output_format="auto",
            width=75
        )
   except Exception as e:
    st.error(f"Ocorreu um erro ao carregar a imagem: {e}")
    
   selected = on_hover_tabs(
        tabName=["Detector de Nota", 'Campo Harmônico', 'Baixar Video', 'Configurações'],
        iconName=['graphic_eq', 'music_note', 'browser_updated', 'browser_updated', 'settings'],
        default_choice=0
   )
    
    # Rodapé no sidebar
   st.markdown("---")
   st.markdown(
        "<div style='position: fixed; bottom: 0; width: 100%; text-align: center;'>"
        "<p><strong>Criado por: Tailon Galvão</strong></p>"
        "<p>Pix do Café☕: (93)981009924</p>"
        "</div>",
        unsafe_allow_html=True
   )

# Redirecionamento para os arquivos de página
if selected == "Detector de Nota":
    page = "detctorSom"
elif selected == "Campo Harmônico":
    page = "harmonico"
elif selected == "Baixar Video":
    page = "baixarVideo"
# elif selected == "Extraindo Metados":
#     page = "image"
elif selected == "Configurações":
    page = "configuracoes"

# Carregar dinamicamente a página selecionada
try:
    page_module = importlib.import_module(page)
    page_module.run()  # Supondo que cada módulo tenha uma função 'run' que executa o conteúdo da página
except ModuleNotFoundError:
    st.error(f"Não foi possível carregar a página '{page}'. Verifique se o caminho está correto.")
