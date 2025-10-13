import cv2
import mediapipe as mp
import time

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

            # coordenadas del dedo índice
            x1 = int(handLms.landmark[8].x * w)
            y1 = int(handLms.landmark[8].y * h)

            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)

            for button in buttonlist:
                bx, by = button.pos # para no tener que escribir button.pos[0] y button.pos[1]
                if bx < x1 < bx + button.width and by < y1 < by + button.height:
                    button.draw(img, hover=True) # redibujar el botón para que se vea que está "pulsado"

                    # si se mantiene el dedo 3 segundo sobre el botón, se considera pulsado
                    if time.time() - click_time > 3:
                        something = True
                        received_val = button.value
                        click_time = time.time()
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

