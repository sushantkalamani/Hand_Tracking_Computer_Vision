import cv2
import mediapipe as mp
import time 
import HandTrackModule as htm
import pyautogui

screen_width, screen_height = pyautogui.size()
cursor_speed = 10


pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        thumb_x, thumb_y = lmList[4][1], lmList[4][2]
        index_finger_x, index_finger_y = lmList[8][1], lmList[8][2]

        distance = ((thumb_x - index_finger_x)**2 + (thumb_y - index_finger_y)**2)**0.5
        
        if distance < 30:
            cv2.circle(img, (thumb_x,thumb_y), 10, (0,255,0), cv2.FILLED)
            cv2.circle(img, (index_finger_x,index_finger_y), 10, (0,255,0), cv2.FILLED)
            pyautogui.click()

        palm_x, palm_y = lmList[5][1], lmList[5][2]

        camera_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  
        camera_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) 
        target_x = int((palm_x / camera_width) * screen_width)
        target_y = int((palm_y / camera_height) * screen_height)

        pyautogui.moveTo(target_x, target_y, duration=cursor_speed / 1000)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)