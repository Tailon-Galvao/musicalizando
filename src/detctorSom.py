import streamlit as st
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time
from collections import Counter, deque
import threading

# Configurações de taxa de amostragem e janela de estabilização
SAMPLE_RATE = 44100
STABILIZATION_WINDOW = 10
FREQUENCY_RANGE = (16, 15546)  # Faixa de frequência de C0 até B9

# Tabela completa de frequências com as oitavas e notas
NOTES_FREQUENCY_MAP = {
    "C0": 16.351, "D0": 18.354, "E0": 20.601, "F0": 21.827, "G0": 24.499, "A0": 27.500, "B0": 30.362,
    "C1": 32.703, "D1": 36.708, "E1": 41.203, "F1": 43.654, "G1": 48.999, "A1": 55.000, "B1": 60.725,
    "C2": 65.406, "D2": 73.416, "E2": 82.407, "F2": 87.307, "G2": 97.999, "A2": 110.00, "B2": 121.45,
    "C3": 130.81, "D3": 146.83, "E3": 164.81, "F3": 174.61, "G3": 196.00, "A3": 220.00, "B3": 242.90,
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "G4": 391.99, "A4": 440.00, "B4": 485.80,
    "C5": 523.25, "D5": 587.33, "E5": 659.26, "F5": 698.46, "G5": 783.99, "A5": 880.00, "B5": 971.60,
    "C6": 1046.5, "D6": 1174.7, "E6": 1318.5, "F6": 1396.9, "G6": 1568.0, "A6": 1760.0, "B6": 1943.2,
    "C7": 2093.0, "D7": 2349.3, "E7": 2637.0, "F7": 2793.8, "G7": 3136.0, "A7": 3520.0, "B7": 3886.4,
    "C8": 4186.0, "D8": 4698.6, "E8": 5274.0, "F8": 5587.7, "G8": 6271.9, "A8": 7040.0, "B8": 7772.8,
    "C9": 8372.0, "D9": 9397.3, "E9": 10548.0, "F9": 11175.0, "G9": 12544.0, "A9": 14080.0, "B9": 15546.0
}

# Função para encontrar a nota mais próxima
def get_closest_note_name(frequency):
    closest_note = None
    min_difference = float('inf')
    for note, note_freq in NOTES_FREQUENCY_MAP.items():
        difference = abs(note_freq - frequency)
        if difference < min_difference:
            min_difference = difference
            closest_note = note
    return closest_note or "Sem detecção"

# Variáveis de controle e buffer
audio_data_buffer = []
note_history = deque(maxlen=STABILIZATION_WINDOW)
running = False
audio_thread = None

# Configuração do PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                 channels=1,
                 rate=SAMPLE_RATE,
                 input=True,
                 frames_per_buffer=4096)

# Função de processamento de áudio
def process_audio():
    global note_history, audio_data_buffer, running

    while running:
        try:
            data = stream.read(4096, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.float32)
            audio_data_buffer.extend(audio_data)

            # Calcula FFT para encontrar frequência dominante
            fft_spectrum = np.abs(np.fft.fft(audio_data))
            freqs = np.fft.fftfreq(len(fft_spectrum), 1 / SAMPLE_RATE)

            # Limita a análise a frequências relevantes
            valid_idxs = np.where((freqs >= FREQUENCY_RANGE[0]) & (freqs <= FREQUENCY_RANGE[1]))
            fft_spectrum = fft_spectrum[valid_idxs]
            freqs = freqs[valid_idxs]

            # Cálculo de frequência dominante usando média ponderada
            freq = np.sum(freqs * fft_spectrum) / np.sum(fft_spectrum)

            # Converte frequência na nota mais próxima
            note = get_closest_note_name(freq)
            note_history.append(note)

            time.sleep(0.1)
        except Exception as e:
            print(f"Erro no processamento de áudio: {e}")
            break

# Função principal para Streamlit
def run():
    global running, audio_thread
    st.header("Detecção de Notas Musicais em Tempo Real")
    st.write("Notas entre C0 e B9 serão identificadas com precisão.")
    st.write("Toque ou cante uma nota para visualização ao vivo.")

    note_display = st.empty()
    graph_placeholder = st.empty()

    run_detection = st.button("Iniciar Detecção")
    stop_detection = st.button("Parar Detecção")

    if run_detection:
        st.write("Detecção iniciada.")
        audio_data_buffer.clear()
        note_history.clear()
        
        running = True
        audio_thread = threading.Thread(target=process_audio)
        audio_thread.start()

    if stop_detection:
        running = False
        if audio_thread is not None:
            audio_thread.join()
        stream.stop_stream()
        stream.close()
        p.terminate()
        st.write("Detecção parada.")
        
        if note_history:
            st.write("Notas detectadas:")
            note_count = Counter(note_history)
            for note, count in note_count.items():
                st.write(f"{note}: {count} vez(es)")

    if running:
        while running:
            if audio_data_buffer:
                current_audio_data = np.array(audio_data_buffer[-SAMPLE_RATE:])
                plt.clf()
                plt.plot(current_audio_data)
                plt.title("Forma de Onda do Áudio")
                plt.xlabel("Tempo (amostras)")
                plt.ylabel("Amplitude")
                plt.xlim(0, len(current_audio_data))
                plt.ylim(-1, 1)
                graph_placeholder.pyplot(plt)

                # Exibe a nota mais comum no histórico recente
                most_common_note = Counter(note_history).most_common(1)[0][0]
                note_display.markdown(f"<h1 style='text-align: center; color: blue;'>{most_common_note}</h1>", unsafe_allow_html=True)

# Inicializa o aplicativo
if __name__ == "__main__":
    run()
