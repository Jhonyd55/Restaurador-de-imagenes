# Inpainting GUI
<img src="https://raw.githubusercontent.com/Jhonyd55/Restaurador-de-imagenes/Restaurador-de-imagenes/images.gif" width="60%"></img> 

Inpainting GUI es una aplicación desarrollada en Python utilizando `tkinter` y `OpenCV` para la restauración de imágenes dañadas mediante técnicas de inpainting. La aplicación permite cargar imágenes dañadas y máscaras opcionales, y ofrece dos métodos de inpainting: Telea y Navier-Stokes. Además, incluye un editor de máscaras para personalizar las áreas a restaurar.

## Características

- Carga de imágenes dañadas.
- Carga de máscaras opcionales.
- Métodos de inpainting: Telea y Navier-Stokes.
- Ajuste de umbral para la creación de máscaras automáticas.
- Barra de progreso durante el proceso de inpainting.
- Guardado de imágenes restauradas.
- Editor de máscaras para crear o modificar máscaras manualmente.

## Requisitos

- Python 3.x
- Tkinter
- OpenCV
- Pillow

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

### Inpainting GUI
<img src="https://raw.githubusercontent.com/Jhonyd55/Restaurador-de-imagenes/Restaurador-de-imagenes/inpainting_app.png" width="30%"></img> 

Para ejecutar la aplicación principal de inpainting:

python inpainting_app.py

## Pasos para Restaurar una Imagen

- Ejecuta inpainting_app.py.

- Carga una imagen dañada haciendo clic en "Cargar Imagen Dañada".

- Opcional: Carga una máscara haciendo clic en "Cargar Máscara (Opcional)".

- Selecciona el método de inpainting (Telea o Navier-Stokes).

- Ajusta el umbral si es necesario.

- Haz clic en "Restaurar Imagen" y espera a que el proceso termine.

- Guarda la imagen restaurada haciendo clic en "Guardar Imagen Restaurada".

### Editor de Máscara
<img src="https://raw.githubusercontent.com/Jhonyd55/Restaurador-de-imagenes/Restaurador-de-imagenes/maskEditor.png" width="30%"></img> 

Para ejecutar el editor de máscara:

python mask_editor.py


## Crear una Máscara

- Ejecuta mask_editor.py.

- Carga una imagen haciendo clic en "Cargar Imagen".

- Dibuja en la imagen para crear la máscara.

- Ajusta el grosor del lápiz si es necesario.

- Guarda la máscara haciendo clic en "Crear Máscara".




"# Restaurador-de-imagenes" 
