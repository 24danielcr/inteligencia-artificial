# Identificación de sonidos estridentes normalizados y no normalizados mediante espectrogramas de audio en redes neuronales convolucionales 


Este proyecto tiene como objetivo el procesamiento, análisis y clasificación de sonidos ambientales utilizando técnicas de aprendizaje automático y procesamiento digital de señales.

## Estructura del Proyecto

- **Espectrogramas/**  
  Carpeta donde se almacenan los espectrogramas generados a partir de los audios, organizados por conjuntos (`train`, `val`, `test`) y clases (`Strident`, `Non-Strident`).

- **Modelos/**  
  Contiene notebooks de entrenamiento y evaluación de modelos de clasificación de audio:
  - `ModeloConAudiosOriginales.ipynb`
  - `ModeloConAudiosProcesados.ipynb`
  - `ModeloConAudiosProcesados50Epocas.ipynb`

- **Sounds-Processed/**  
  Audios ya procesados y listos para ser usados en entrenamiento, validación y prueba.

- **Sounds-Raw/**  
  Audios originales sin procesar, organizados por clase.

- **Sounds-Raw-Separated/**  
  Audios originales separados en carpetas de entrenamiento, validación y prueba.

- **src/**  
  Código fuente del proyecto, incluyendo scripts para limpieza de audio, generación de espectrogramas y utilidades varias:
  - `Sound-Cleaning.py`: Limpieza y preprocesamiento de audios.
  - `espectro.py`: Generación de espectrogramas a partir de archivos de audio.

- **SoundsEspecifications.txt**  
  Especificaciones y fuentes de los sonidos utilizados.

## Requisitos

- Python 3.7 o superior
- Bibliotecas principales: `librosa`, `numpy`, `matplotlib`, `scikit-learn`, `tensorflow` (o `keras`), entre otras.

## Ejecución

1. **Preprocesamiento de audios:**  
   Ejecuta los scripts en `src/Sound-Cleaning.py` para limpiar y preparar los audios.

2. **Generación de espectrogramas:**  
   Usa `src/espectro.py` para convertir los audios en espectrogramas.

3. **Entrenamiento de modelos:**  
   Abre y ejecuta los notebooks en la carpeta `Modelos/` para entrenar y evaluar los modelos de clasificación.
