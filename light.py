import cv2
import numpy as np

cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()
light_on = 0
light_off = 0
count = 0
ret, frame2 = cap.read()
left, center, right = False, False, False
x = 300
mask = np.zeros((200, 400))
while cap.isOpened():
    ret, frame2 = cap.read()
    g1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(g1, g2)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    contour, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contour) > 0:
        contour = max(contour, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)


    if not(left) and not(right):
        if x < 150:
            left = True
        elif x > 450:
            right = True
    elif left:
        if x > 150 and x < 450 and not(center):
            center = True
        if x > 450:
            if center:
                mask = np.zeros((200, 400))
                light_on += 1
                mask = cv2.putText(mask, 'PERSON ENTERED='+str(light_on), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255), 2)
                center = False
                left = False
            else:
                right = True
                left = False
    elif right:
        if x > 150 and x < 450 and not(center):
            center = True
        if x < 150:
            if center:
                mask = np.zeros((200, 400))
                light_on-=1
                mask = cv2.putText(mask, 'PERSON LEAVE='+str(light_on),  (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255), 2)
                center = False
                right = False
            else:
                left = True
                right = False

    cv2.imshow("CAMERA", frame1)
    cv2.imshow("CAMERA1", thresh)
    cv2.imshow('STATUS', mask)
    if light_on == 1:
        if count != 1:
            count = 1
            #sms()
            print('on')

    ret, frame1 = cap.read()
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
