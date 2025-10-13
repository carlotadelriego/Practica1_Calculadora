# Calculadora Basada en Gestos — Práctica 1. Sistemas Inteligentes Interactivos

**Universidad:** Universidad Intercontinental de la Empresa (UIE)  
**Autora:** Carlota Fernández del Riego  
**Profesor:** David Rivas Villar  
**Fecha:** 14 Octubre 2025  

---

## Objetivo de la práctica

Diseñar e implementar una **calculadora controlada mediante gestos**, utilizando la **cámara web** y técnicas de **visión por computador**.  
El sistema debe detectar la mano del usuario mediante **MediaPipe Hands** y permitir realizar operaciones básicas como son la suma, la resta, la multiplicación, la división y el borrado **sin tocar el teclado**, solo con gestos o manteniendo el dedo índice sobre los botones virtuales. Además, el sistema debe de tener en cuenta la posición y la orientación de los dedos para detectarlos a través de la cámara y traducirlos en una acción.


---

## Tecnologías utilizadas

Para poder realizar esta práctica se han necesitado tecnologías como:

- **Python 3.10+**
- [OpenCV](https://opencv.org/) → interfaz visual y control de cámara  
- [MediaPipe Hands](https://developers.google.com/mediapipe) → detección y seguimiento de manos  
- [Docker](https://www.docker.com/) + Makefile → entorno reproducible  

- **time** (módulo de Python) → control de estabilidad y tiempo de espera  

---

## Ejecución del proyecto

### 1. Requisitos previos
Instalar las dependencias (se puede usar el archivo `requirements.txt`): `pip install -r requirements.txt`


### 2. 



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