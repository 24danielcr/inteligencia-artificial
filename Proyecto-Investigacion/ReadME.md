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

## Ejecución Local y Entorno Virtual

### 1. Crear y activar un entorno virtual

En la terminal, navega a la carpeta del proyecto y ejecuta:

```bash
python3 -m venv venv
```

Activa el entorno virtual:

- En **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```
- En **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```

### 2. Instalar dependencias

Con el entorno virtual activado, instala las dependencias usando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Si necesitas generar el archivo `requirements.txt` desde tu entorno actual, usa:

```bash
pip freeze > requirements.txt
```

### 3. Flujo de ejecución recomendado

1. **Preprocesamiento de audios:**  
   Ejecuta el script `src/Sound-Cleaning.py` para limpiar y preparar los audios.

2. **Generación de espectrogramas:**  
   Usa `src/espectro.py` para convertir los audios en espectrogramas.

3. **Entrenamiento y evaluación de modelos:**  
   Abre y ejecuta los notebooks en la carpeta `Modelos/` para entrenar y evaluar los modelos de clasificación.

### 4. Uso en Google Colab

Para una experiencia más sencilla y visual, puedes subir los notebooks (`.ipynb`) de la carpeta `Modelos/` a [Google Colab](https://colab.research.google.com/) y ejecutarlos directamente desde ahí, lo que facilita la visualización de resultados y el manejo de dependencias.
