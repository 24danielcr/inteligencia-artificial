# Manual Sound-Cleaning.py 

## Requerimientos
Se necesitan los paquetes `numpy`, `matplotlib` y `librosa`. Se pueden instalar de la siguiente manera:

```
pip install numpy matplotlib librosa
```

En el caso de `FFmpeg`:

### macOS
```
brew install ffmpeg
```

### Windows
```
choco install ffmpeg -y
```

### Linux
```
sudo apt install ffmpeg
```

## Rutas de Datos
Rutas están ya configuradas en el código.

## Opciones de audio
Opciones de audio están configuradas dentro del código como variables globales.

## Opciones de extensión
Por defecto se utiliza **.mp3*, variable global en el código.

## Opciones de Normalización
El programa por defecto sólo normaliza el volumen de los audios, los convierte
a **.mp3* y divide los datos en tres carpeta diferentes: `train / test / val`. Se corre de esta manera:
```
python3 .\Sound-Cleaning.py
```

Si se quiere normalizar los espectrogramas a {0, 1} y eliminar sonido de fondo
innecesario, correr el programa de la siguiente manera:

```
python3 .\Sound-Cleaning.py -cache
```