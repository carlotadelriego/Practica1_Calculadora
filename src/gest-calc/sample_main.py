import cv2
import mediapipe as mp
import time

# FUNCIÓN PARA DETECTAR SI UN DEDO ESTÁ LEVANTADO
def fingers_up(hand_landmarks):
    lm = hand_landmarks.landmark
    fingers = []

    # Pulgar (horizontal)
    fingers.append(lm[4].x < lm[3].x)

    # Otros 4 dedos (vertical)
    for tip in [8, 12, 16, 20]:
        fingers.append(lm[tip].y < lm[tip - 2].y)

    return fingers.count(True)




# CLASE PARA LOS BOTONES DE LA CALCULADORA
class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img, hover=False):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)

        text_x = self.pos[0] + self.width // 2 - 15
        text_y = self.pos[1] + self.height // 2 + 15

        cv2.putText(img, self.value, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN,
                    3, (50, 50, 50), 3)



# CONFIGURACION DE LA CAMARA
# MUST be configured for each system
cap = cv2.VideoCapture(0) # here would be 0 or 1 for most systems, but mine is 2
# it is the webcam address, in my case in /dev/video2

#input image size, based on your webcam
WIDTH = 1920
HEIGHT = 1080
cap.set(3, WIDTH)
cap.set(4, HEIGHT)



# CUADRÍCULA DE LOS BOTONES
# basic list of buttons, may be changed (changes must be justified)
buttonListValues = [['C', '<'],
                    ['7', '8', '9', '/'],  # ÷ cant be rendered, so well have to do with / :/
                    ['4', '5', '6', '*'],
                    ['1', '2', '3', '-'],
                    ['0', '.', '=', '+']]

buttonlist = []
for y in range(5):
    for x in range(4):
        if y == 0 and x >= 2:  # first row only has 2 buttons (C and <), so kinda special case
            break

        xpos = int(WIDTH - 500 + x * 100)
        ypos = int(HEIGHT * 0.15 + y * 100)

        # first row special case, second button needs to be shifted
        if y == 0 and x == 1: #not the most elegant
            xpos += 100

        if y == 0:
            width = 200
            buttonlist.append(Button((xpos, ypos), width, 100, buttonListValues[y][x]))
        else:
            buttonlist.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))



# INICIALIZAR MEDIAPIPE HANDS
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)



# VARIABLES DE CONTROL
operation = ""
click_time = 0
last_count = -1 # último número de dedos detectado
stable_frames = 0   # contador de frames estables
hover_time = 0
hover_target = None
hover_start = 0.0




# BUCLE PRINCIPAL
while True:
    success, img = cap.read()
    if not success:
        break

    h, w, c = img.shape # alto, ancho, canales
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convertir a RGB
    results = hands.process(img_rgb) 


    operation_x = int(WIDTH - 500)
    operation_y = int(HEIGHT * 0.05)

    cv2.rectangle(img, (operation_x, operation_y), (operation_x + 400, operation_y + 120),
                  (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (operation_x, operation_y), (operation_x + 400, operation_y + 120),
                  (50, 50, 50), 3)


    # DIBUJAR BOTONES
    for button in buttonlist:
        button.draw(img)



    # DETECCION DE MANOS 
    # when something triggers, the calculator should actually calculate
    # the something should be programmed by you, of course
    something = False
    received_val = ""

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            # detectar si hay 1 dedo levantado y contar cuántos dedos están levantados
            count = fingers_up(handLms)

            # Comprobar si el gesto se mantiene estable
            if count == last_count:
                stable_frames += 1
            else:
                stable_frames = 0
                last_count = count


            # Mostrar en pantalla el número de dedos detectado
            cv2.putText(img, f"Dedos levantados: {count}", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)
            

            # GESTOS PERSONALIZADOS PARA LA CALCULADORA

            # Creamos la lista de dedos levantados (True = arriba)
            lm = handLms.landmark
            fingers = []
            fingers.append(lm[4].x < lm[3].x)  # Pulgar (horizontal)
            for tip in [8, 12, 16, 20]:
                fingers.append(lm[tip].y < lm[tip - 2].y)

            # === MAPEO DE GESTOS ===
            #  ✊ Puño cerrado → borrar
            if fingers == [False, False, False, False, False] and time.time() - click_time > 3:
                operation = ""
                cv2.putText(img, "BORRANDO...", (250, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 255, 0), 4)
                click_time = time.time()

            # ☝️ Solo índice → seleccionar botón de la calculadora
            elif fingers == [False, True, False, False, False]:
                x1 = int(handLms.landmark[8].x * w)
                y1 = int(handLms.landmark[8].y * h)
                cv2.circle(img, (x1, y1), 10, (0, 255, 255), cv2.FILLED)

                for button in buttonlist:
                    bx, by = button.pos
                    if bx < x1 < bx + button.width and by < y1 < by + button.height:
                        button.draw(img, hover=True)

                        # Si se mantiene 3s sobre la tecla, se selecciona
                        if 'hover_start' not in locals():
                            hover_start = time.time()
                            hover_target = button.value

                        if hover_target != button.value:
                            hover_target = button.value
                            hover_start = time.time()

                        if time.time() - hover_start > 3:
                            operation += button.value
                            cv2.putText(img, f"{button.value}", (250, 200),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
                            hover_start = time.time()  # reinicia contador
                        break
                else:
                    hover_target = None


            # ✌️ Índice + corazón → número 2
            elif fingers == [False, True, True, False, False] and time.time() - click_time > 3:
                operation += "2"
                click_time = time.time()

            # 🤘 Índice + meñique → suma (+)
            elif fingers == [False, True, False, False, True] and time.time() - click_time > 3:
                operation += "+"
                click_time = time.time()

            # 🤙 Pulgar + meñique → multiplicación (*)
            elif fingers == [True, False, False, False, True] and time.time() - click_time > 3:
                operation += "*"
                click_time = time.time()

            # ✋ Cuatro dedos (pulgar abajo) → resta (-)
            elif fingers == [False, True, True, True, True] and time.time() - click_time > 3:
                operation += "-"
                click_time = time.time()

            # 🖐️ Cinco dedos → número 5
            elif fingers == [True, True, True, True, True] and time.time() - click_time > 3:
                operation += "5"
                click_time = time.time()

            # 👍 Pulgar en vertical (hacia arriba) → calcular (=)
            elif fingers[0] and not any(fingers[1:]) and time.time() - click_time > 3:
                cv2.putText(img, "CALCULANDO...", (250, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 0, 0), 4)
                try:
                    operation = str(eval(operation))
                except:
                    operation = "Error"
                click_time = time.time()



            # DIBUJAR CÍRCULO EN DEDO ÍNDICE
            # coordenadas del dedo índice
            x1 = int(handLms.landmark[8].x * w)
            y1 = int(handLms.landmark[8].y * h)
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)

            for button in buttonlist:
                bx, by = button.pos
                if bx < x1 < bx + button.width and by < y1 < by + button.height:
                    button.draw(img, hover=True)

                    # usar hover_time separado del click_time
                    if time.time() - hover_time > 3:
                        something = True
                        received_val = button.value
                        hover_time = time.time()
                    break


    # GESTIONAR LA OPERACION - LÓGICA DE LA CALCULADORA
    if something:
        if received_val == "=":
            try:
                operation = str(eval(operation))
            except:
                operation = "Error"
        elif received_val == "C":  # Reset
            operation = ""
        elif received_val == "<":  # remove char
            operation = operation[:-1]
        else:
            operation += received_val
        delayCounter = 1


    # MOSTRAR LA OPERACION EN PANTALLA
    cv2.putText(img, operation, (operation_x + 10, operation_y + 75),
                cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    cv2.imshow('Calculadora por GESTOS', img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

