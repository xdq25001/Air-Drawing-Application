import cv2
import mediapipe as mp
import numpy as np

# setup mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0) #if I put 0, it uses my phone's camera

# 1. Create a blank canvas to draw on
canvas = None
# Store previous finger position
prev_x, prev_y = None, None

colors = [(255,0,0), (0,255,0), (0,0,255), (0,255,255)]
color_index = 0
current_color = colors[color_index]
color_delay = 0

while True:
    success, img = cap.read()
    if not success: 
        break
    
    img = cv2.flip(img, 1) #flips camera so it's easier for user to see what they're drawing
    if canvas is None:
        canvas = np.zeros_like(img) # Initialize canvas with same dimensions as webcam

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            h, w, c = img.shape
            # index fingertip
            index_tip = handLms.landmark[8]
            # index middle joint
            index_joint = handLms.landmark[6]

            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            index_up = handLms.landmark[8].y < handLms.landmark[6].y
            middle_up = handLms.landmark[12].y < handLms.landmark[10].y
            ring_up = handLms.landmark[16].y < handLms.landmark[14].y
            pinky_up = handLms.landmark[20].y < handLms.landmark[18].y
            thumb_up = handLms.landmark[4].y < handLms.landmark[2].y

            open_hand = index_up and middle_up and ring_up and pinky_up and thumb_up

            if middle_up and index_up and color_delay == 0:
                color_index = (color_index + 1) % len(colors)
                current_color = colors[color_index]
                color_delay = 100

            if color_delay > 0:
                color_delay -= 1

            if open_hand:
                canvas = np.zeros_like(img)
                prev_x, prev_y = None, None

            elif index_up and not middle_up:
                if prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), current_color, 5)

                prev_x, prev_y = x, y

            else:
                prev_x, prev_y = None, None
    else:
        # 3. Reset position when hand is lost (the "pen lift")
        prev_x, prev_y = None, None

    # Merge the canvas with the webcam image
    img = cv2.addWeighted(img, 0.5, canvas, 1, 0)
    
    cv2.imshow("Air Drawing", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()

