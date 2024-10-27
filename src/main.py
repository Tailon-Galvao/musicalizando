import streamlit as st
import numpy as np
from st_on_hover_tabs import on_hover_tabs
import importlib

css_file_path = 'css/style.css'
image_path='/img/music.png'

# Configurações da página
st.set_page_config(page_title="Musicalizando", layout="wide")

# Aplicar estilo CSS personalizado
st.markdown('<style>' + open(css_file_path).read() + '</style>', unsafe_allow_html=True)

# Sidebar com imagem e tabs de navegação
with st.sidebar:
    st.image(
        image_path,
        output_format="auto",
        width=75
    )
    
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
