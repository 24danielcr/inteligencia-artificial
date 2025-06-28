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
            plt.savefig(ruta_salida, bbox_inches='tight', pad_inches=0, dpi=50)
            plt.close()
            
        except Exception as e:
            print(f"Error procesando {archivo.name}: {e}")
    
    print(f"Proceso completado. Espectrogramas guardados en: {carpeta_salida}")


if __name__ == "__main__":
    # Stridents
    carpeta_audios = "Proyecto-Investigacion/Sounds-Raw/Non-Strident"
    carpeta_espectros = "Proyecto-Investigacion/Espectrogramas/Sounds-Raw/Non-Strident"

    audio_a_espectrograma(carpeta_audios, carpeta_espectros, tipo='mel')

    carpeta_audios = "Proyecto-Investigacion/Sounds-Raw/Strident"
    carpeta_espectros = "Proyecto-Investigacion/Espectrogramas/Sounds-Raw/Strident"
    audio_a_espectrograma(carpeta_audios, carpeta_espectros, tipo='mel')
##------------------------------------------------------------------------------------------------

    carpeta_audios = "Proyecto-Investigacion/Sounds-Processed/test/Non-Strident"
    carpeta_espectros = "Proyecto-Investigacion/Espectrogramas/Sounds-Processed/test/Non-Strident"

    audio_a_espectrograma(carpeta_audios, carpeta_espectros, tipo='mel')

    carpeta_audios = "Proyecto-Investigacion/Sounds-Processed/test/Strident"
    carpeta_espectros = "Proyecto-Investigacion/Espectrogramas/Sounds-Processed/test/Strident"

    audio_a_espectrograma(carpeta_audios, carpeta_espectros, tipo='mel')
##------------------------------------------------------------------------------------------------
    carpeta_audios = "Proyecto-Investigacion/Sounds-Processed/train/Strident"
    carpeta_espectros = "Proyecto-Investigacion/Espectrogramas/Sounds-Processed/train/Strident"

    audio_a_espectrograma(carpeta_audios, carpeta_espectros, tipo='mel')

    carpeta_audios = "Proyecto-Investigacion/Sounds-Processed/train/Non-Strident"
    carpeta_espectros = "Proyecto-Investigacion/Espectrogramas/Sounds-Processed/train/Non-Strident"

    audio_a_espectrograma(carpeta_audios, carpeta_espectros, tipo='mel')
##------------------------------------------------------------------------------------------------
    carpeta_audios = "Proyecto-Investigacion/Sounds-Processed/val/Strident"
    carpeta_espectros = "Proyecto-Investigacion/Espectrogramas/Sounds-Processed/val/Strident"

    audio_a_espectrograma(carpeta_audios, carpeta_espectros, tipo='mel')

    carpeta_audios = "Proyecto-Investigacion/Sounds-Processed/val/Non-Strident"
    carpeta_espectros = "Proyecto-Investigacion/Espectrogramas/Sounds-Processed/val/Non-Strident"

    audio_a_espectrograma(carpeta_audios, carpeta_espectros, tipo='mel')