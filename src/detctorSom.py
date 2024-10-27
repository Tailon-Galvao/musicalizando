import streamlit as st
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import math
import time
from collections import Counter

# Configurações
SAMPLE_RATE = 44100  # Taxa de amostragem (Hz)
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Função para converter frequência em nota musical
def freq_to_note_name(frequency):
    if frequency == 0:
        return "Sem detecção"
    
    # Cálculo da nota
    A4 = 440.0  # Frequência do A4 (padrão)
    C0 = A4 * math.pow(2, -4.75)  # Calcula a frequência de C0
    h = round(12 * math.log2(frequency / C0))  # Distância em semitons de C0
    octave = h // 12  # Determina a oitava
    n = h % 12  # Determina a nota
    return f"{NOTE_NAMES[n]}{octave}"

# Lista para armazenar dados de áudio e notas
audio_data_buffer = []
notes = []

# Função de callback para processar áudio
def audio_callback(indata, frames, time, status):
    if status:
        print(status)

    # Converte o áudio para array NumPy
    audio_data = np.squeeze(indata)
    
    # Armazena o áudio no buffer
    audio_data_buffer.extend(audio_data)

    # Aplica FFT para obter as frequências
    fft_spectrum = np.abs(np.fft.fft(audio_data))
    freqs = np.fft.fftfreq(len(fft_spectrum), 1 / SAMPLE_RATE)

    # Encontrar a frequência dominante
    idx = np.argmax(fft_spectrum[:len(fft_spectrum)//2])  # Só usamos a primeira metade
    freq = abs(freqs[idx])

    # Converte frequência em nota
    note = freq_to_note_name(freq)
    
    # Armazena a nota
    notes.append(note)

# Função para plotar a forma de onda
def plot_waveform(audio_data):
    plt.figure(figsize=(10, 4))
    plt.plot(audio_data, color='blue')
    plt.title("Forma de Onda do Áudio")
    plt.xlabel("Tempo (amostras)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.xlim(0, len(audio_data))
    plt.ylim(-1, 1)
    plt.tight_layout()
    return plt

# Função principal
def run():
    st.header("Detecção de Notas Musicais em Tempo Real", divider=True)
    st.write('As notas vão de C0 (Dó na oitava 0) até B0 (Si na oitava 0), e assim por diante..') 
    st.write('O número ao lado da nota refere-se à oitava em que a nota se encontra.')

    
    # Criar placeholders
    note_display = st.empty()  # Placeholder para exibir a nota
    graph_placeholder = st.empty()  # Placeholder para o gráfico

    # Controle de execução
    run_detection = st.button("Iniciar Detecção")
    stop_detection = st.button("Parar Detecção")

    if run_detection:
        st.write("Detecção iniciada. Fale ou toque uma nota.")
        audio_data_buffer.clear()
        notes.clear()
        
        # Inicia o stream de áudio
        with sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE):
            while True:
                time.sleep(0.1)  # Espera um curto período para evitar uso excessivo de CPU
                
                # Atualiza a forma de onda em tempo real
                if audio_data_buffer:
                    # Plota a forma de onda
                    current_audio_data = np.array(audio_data_buffer[-SAMPLE_RATE:])  # Captura os últimos segundos
                    plt.clf()  # Limpa o gráfico anterior
                    plot_waveform(current_audio_data)  # Plota a forma de onda atualizada
                    graph_placeholder.pyplot(plt)  # Exibe o gráfico

                    # Exibe a última nota detectada
                    current_note = notes[-1]  # Pega a última nota detectada
                    note_display.markdown(f"<h1 style='text-align: center; color: blue;'>{current_note}</h1>", unsafe_allow_html=True)

                # Checa se o botão "Parar Detecção" foi pressionado
                if stop_detection:
                    break

    if stop_detection:
        st.write("Detecção parada.")
        
        # Exibe as notas detectadas
        if notes:
            st.write("Notas detectadas:")
            note_count = Counter(notes)  # Conta as ocorrências de cada nota
            for note, count in note_count.items():
                st.write(f"{note}: {count} vez(es)")

# Inicializa o aplicativo
if __name__ == "__main__":
    run()
