import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

def audio_a_espectrograma(carpeta_entrada, carpeta_salida, tipo='mel'):

    Path(carpeta_salida).mkdir(parents=True, exist_ok=True)
    
    # Extensiones soportadas
    extensiones = ['.wav', '.mp3', '.flac', '.m4a', '.ogg']
    
    archivos_audio = []
    for ext in extensiones:
        archivos_audio.extend(Path(carpeta_entrada).glob(f'*{ext}'))
    
    print(f"Encontrados {len(archivos_audio)} archivos de audio")
    
    for i, archivo in enumerate(archivos_audio):
        try:
            print(f"Procesando {i+1}/{len(archivos_audio)}: {archivo.name}")
            
            y, sr = librosa.load(archivo)
            
            if tipo == 'mel':
                S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
                S_db = librosa.power_to_db(S, ref=np.max)
            elif tipo == 'stft':
                D = librosa.stft(y)
                S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
            

            plt.figure(figsize=(10, 4))
            librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='mel' if tipo=='mel' else 'hz')
            plt.axis('off')  # Sin ejes
            plt.tight_layout(pad=0)
            

            nombre_salida = archivo.stem + '_spectrogram.png'
            ruta_salida = Path(carpeta_salida) / nombre_salida
            plt.savefig(ruta_salida, bbox_inches='tight', pad_inches=0, dpi=100)
            plt.close()
            
        except Exception as e:
            print(f"Error procesando {archivo.name}: {e}")
    
    print(f"Proceso completado. Espectrogramas guardados en: {carpeta_salida}")


if __name__ == "__main__":
    # Stridents
    carpeta_audios = "Sounds-Processed/Strident"
    carpeta_espectros = "Espectrogramas/Strident"

    #audio_a_espectrograma(carpeta_audios, carpeta_espectros, tipo='mel')

    # Non-Stridents
    carpeta_audios = "Sounds-Processed/Non-Strident"
    carpeta_espectros = "Espectrogramas/Non-Strident"

    audio_a_espectrograma(carpeta_audios, carpeta_espectros, tipo='mel')