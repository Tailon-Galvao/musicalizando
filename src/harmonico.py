import streamlit as st
import matplotlib.pyplot as plt

# Função para calcular o campo harmônico da nota
def campo_harmonico(nota):
    acordes = {
        'C': ['C', 'Dm', 'Em', 'F', 'G', 'Am', 'Bdim'],
        'C#': ['C#', 'D#m', 'E#m', 'F#', 'G#', 'A#m', 'B#dim'],
        'D': ['D', 'Em', 'F#m', 'G', 'A', 'Bm', 'C#dim'],
        'D#': ['D#', 'E#m', 'Gm', 'G#', 'A#', 'Cm', 'Ddim'],
        'E': ['E', 'F#m', 'G#m', 'A', 'B', 'C#m', 'D#dim'],
        'F': ['F', 'Gm', 'Am', 'Bb', 'C', 'Dm', 'Edim'],
        'F#': ['F#', 'G#m', 'A#m', 'B', 'C#', 'D#m', 'E#dim'],
        'G': ['G', 'Am', 'Bm', 'C', 'D', 'Em', 'F#dim'],
        'G#': ['G#', 'A#m', 'B#m', 'C#', 'D#', 'F#m', 'G#dim'],
        'A': ['A', 'Bm', 'C#m', 'D', 'E', 'F#m', 'G#dim'],
        'A#': ['A#', 'B#m', 'C#m', 'D#', 'E#', 'Gm', 'A#dim'],
        'B': ['B', 'C#m', 'D#m', 'E', 'F#', 'G#m', 'A#dim'],
    }
    return acordes.get(nota.upper(), "Nota inválida! Tente novamente.")

def run():
    # Título da aplicação
    st.header("Campo Harmônico")

    # Input do usuário
    nota_usuario = st.text_input("Insira uma nota musical (C, D, E, F, G, A, B, C#, D#, F#, G#, A#):")

    # Inicializar a variável resultado
    resultado = None

    # Botão para mostrar o campo harmônico
    if st.button("Mostrar Notas"):
        if nota_usuario:
            resultado = campo_harmonico(nota_usuario)
            if isinstance(resultado, list):
                st.write("Campo Harmônico:")

                # Frequências das notas
                frequencias = [note_to_frequency(nota) for nota in resultado]

                # Criar gráfico
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(resultado, frequencias, color='green', width=0.3)  # Diminuindo a largura das colunas
                ax.set_facecolor('black')  # Fundo preto
                ax.set_title("Campo Harmônico", color='white')
                ax.set_ylabel("Frequência (Hz)", color='white')
                ax.set_xlabel("Notas", color='white')
                ax.tick_params(axis='x', colors='white')  # Cores dos rótulos do eixo X
                ax.tick_params(axis='y', colors='white')  # Cores dos rótulos do eixo Y

                # Adicionando a nota e a frequência em cada barra
                for i, v in enumerate(frequencias):
                    ax.text(i, v + 5, f'{resultado[i]}\n{v} Hz', ha='center', color='white')

                # Mostrar o gráfico na Streamlit
                st.pyplot(fig)

                # Mostrar cada nota
                for nota in resultado:
                    st.write(f"**Nota:** {nota} - **Frequência:** {note_to_frequency(nota)} Hz")
            else:
                st.warning(resultado)
        else:
            st.warning("Por favor, insira uma nota antes de clicar em 'Mostrar Notas'.")

def note_to_frequency(note):
    """Converte uma nota musical para sua frequência (em Hz)"""
    note_frequencies = {
        'C': 261.63,
        'C#': 277.18,
        'D': 293.66,
        'D#': 311.13,
        'E': 329.63,
        'F': 349.23,
        'F#': 369.99,
        'G': 392.00,
        'G#': 415.30,
        'A': 440.00,
        'A#': 466.16,
        'B': 493.88,
        'Dm': 293.66,  # Nota base do acorde Dm
        'Em': 329.63,  # Nota base do acorde Em
        'F#m': 369.99, # Nota base do acorde F#m
        'Gm': 392.00,  # Nota base do acorde Gm
        'Am': 440.00,  # Nota base do acorde Am
        'Bm': 493.88,  # Nota base do acorde Bm
        'Bdim': 493.88, # Nota base do acorde Bdim
        'Cdim': 261.63, # Nota base do acorde Cdim
        'Ddim': 293.66, # Nota base do acorde Ddim
        'Edim': 329.63, # Nota base do acorde Edim
        'F#dim': 369.99,# Nota base do acorde F#dim
        'G#dim': 415.30,# Nota base do acorde G#dim
        'A#dim': 466.16,# Nota base do acorde A#dim
    }
    return note_frequencies.get(note, 0)

# Executar a função
if __name__ == "__main__":
    run()
