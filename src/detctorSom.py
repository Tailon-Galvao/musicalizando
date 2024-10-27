import streamlit as st
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import math
import time
from collections import Counter
import threading

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
running = False
audio_thread = None  # Inicializa audio_thread como None

# Configuração do PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                 channels=1,
                 rate=SAMPLE_RATE,
                 input=True,
                 frames_per_buffer=1024)

def process_audio():
    global notes, audio_data_buffer, running

    while running:
        try:
            # Lê dados de áudio
            data = stream.read(1024, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.float32)
            audio_data_buffer.extend(audio_data)

            # Aplica FFT para obter as frequências
            fft_spectrum = np.abs(np.fft.fft(audio_data))
            freqs = np.fft.fftfreq(len(fft_spectrum), 1 / SAMPLE_RATE)

            # Encontrar a frequência dominante
            idx = np.argmax(fft_spectrum[:len(fft_spectrum)//2])  # Só usamos a primeira metade
            freq = abs(freqs[idx])

            # Converte frequência em nota
            note = freq_to_note_name(freq)
            notes.append(note)

            time.sleep(0.1)  # Espera um curto período para evitar uso excessivo de CPU
        except Exception as e:
            print(f"Erro no processamento de áudio: {e}")
            break

# Função principal
def run():
    global running, audio_thread
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
        
        running = True  # Inicia a flag de execução
        audio_thread = threading.Thread(target=process_audio)
        audio_thread.start()

        while running:
            # Atualiza a forma de onda em tempo real
            if audio_data_buffer:
                # Plota a forma de onda
                current_audio_data = np.array(audio_data_buffer[-SAMPLE_RATE:])  # Captura os últimos segundos
                plt.clf()  # Limpa o gráfico anterior
                plt.plot(current_audio_data)
                plt.title("Forma de Onda do Áudio")
                plt.xlabel("Tempo (amostras)")
                plt.ylabel("Amplitude")
                plt.xlim(0, len(current_audio_data))
                plt.ylim(-1, 1)
                graph_placeholder.pyplot(plt)

                # Exibe a última nota detectada
                current_note = notes[-1] if notes else "Sem detecção"  # Pega a última nota detectada
                note_display.markdown(f"<h1 style='text-align: center; color: blue;'>{current_note}</h1>", unsafe_allow_html=True)

            # Checa se o botão "Parar Detecção" foi pressionado
            if stop_detection:
                break

    if stop_detection:
        running = False  # Para o processamento de áudio
        if audio_thread is not None:  # Verifica se a thread foi criada
            audio_thread.join()  # Aguarda o término da thread de áudio
        stream.stop_stream()
        stream.close()
        p.terminate()
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
