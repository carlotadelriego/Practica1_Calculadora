# Calculadora Basada en Gestos — Práctica 1

**Universidad:** Universidad Intercontinental de la Empresa
**Asignatura:** Sistemas Inteligentes Interactivos
**Autora:** Carlota Fernández del Riego  
**Profesor:** David Rivas Villar  
**Fecha:** 14 Octubre 2025  

---

## Objetivo de la práctica

Diseñar e implementar una **calculadora controlada mediante gestos**, utilizando la **cámara web** y técnicas de **visión por computador**.  
El sistema debe detectar la mano del usuario mediante **MediaPipe Hands** y permitir realizar operaciones básicas como son la suma, la resta, la multiplicación, la división y el borrado **sin tocar el teclado**, solo con gestos o manteniendo el dedo índice sobre los botones virtuales. Además, el sistema debe tener en cuenta la posición y la orientación de los dedos para detectarlos a través de la cámara y traducirlos a una acción.


---

## Tecnologías empleadas

Para poder realizar esta práctica se han necesitado tecnologías como:

- **Python 3.10+**
- [OpenCV](https://opencv.org/) para la interfaz visual y control de cámara  
- [MediaPipe Hands](https://developers.google.com/mediapipe) para la detección y el seguimiento de las manos  
- [Docker](https://www.docker.com/) + Makefile para el entorno reproducible  

- **time** (módulo de Python) para el control de la estabilidad y el tiempo de espera  

---

## Ejecución del proyecto

### 1. Requisitos previos
Instalar las dependencias (para ello se puede usar el archivo `requirements.txt`): `pip install -r requirements.txt`

### 2. Verificación del funcionamiento de la cámara
Antes de iniciar la calculadora, es recomendable probar que la cámara funciona correctamente ejecutando el código `webcam_test.py``
    *Nota: para los usuarios de Mac es probable que se deba usar la cámara 0, cap = cv2.VideoCapture(0), y eliminar la línea `gpus all` del archivo `Makefile`*
Si se ve la imagen de la cámara en una ventana llamada “Video2 Full HD”, se puede continuar con la ejecución del programa principal.

### 3. Ejecución de la Calculadora por Gestos
Ejecuta el script principal desde la terminal con el comando `python calculadora_gestos.py`
    *RECUERDA: Si tu cámara no se abre, cambia el índice en la línea cap = cv2.VideoCapture(0) por cap = cv2.VideoCapture(1) o cap = cv2.VideoCapture(2) según tu dispositivo.*

### 4. Control por gestos
Una vez abierta la ventana de la cámara, MediaPipe detectará tu mano y podrás usar los siguientes gestos para usar la calculadora:

       GESTO                           ACCIÓN
    Puño cerrado	                Borrar toda la operación
    Solo índice	                    Seleccionar botón (manteniendo 3 segundos sobre el número/signo)
    Índice + corazón                Insertar número “2”
    Índice + meñique                Insertar signo “+”
    Pulgar + meñique                Insertar signo “*”
    Cuatro dedos                    Insertar signo “-”
    Cinco dedos	                    Insertar número “5”
    Pulgar arriba	                Calcular resultado de la operación (=)

Pulsa `q` para salir del programa.

### 5. Ejemplo de uso del programa
1. Escribe en la terminal `python calculadora_gestos.py`,recuerda estar siempre en la ruta correcta del programa (`cd + ruta del archivo`)
2. Apunta con el dedo índice al número deseado.
3. Usa el gesto correspondiente para sumar, restar o multiplicar.
4. Levanta el pulgar para calcular el resultado.
5. El resultado se mostrará en la pantalla de la calculadora.



---

### Funcionamiento general

El sistema:
1. Se inicia la cámara y se detecta la mano del usuario.
2. El sistema interpreta la posición de los dedos mediante MediaPipe Hands.
3. Se traducen los patrones de los dedos levantados a gestos predefinidos.
4. Se muestra en pantalla una calculadora virtual con botones renderizados en OpenCV.
5. Se permiten escribir números y operaciones tanto por gestos como apuntando con el dedo índice.
6. Se evalúa la operación matemática al hacer el gesto de “pulgar hacia arriba” o desde el botón = situado en la antalla.


---

### Gestos implementados

### Interfaz

### Lógica del sistema

### Estructura del proyecto

### Vista previa

### Conclusiones