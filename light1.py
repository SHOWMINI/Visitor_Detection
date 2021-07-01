import cv2
import numpy as np
cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()
light_on = 0
people_visited = 0
people_left = 0
people_in_shop = 0
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
    for c in contour:
       if cv2.contourArea(c) < 2000:
           continue
       else:
           x, y, w, h = cv2.boundingRect(c)
           #cv2.drawContours(frame1, c, -1, (0, 255, 0), 5)

           cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)


    if not(left) and not(right):
        if x < 110:
            left = True
        elif x > 500:
            right = True
    elif left:
        if x > 110 and x < 500 and not(center):
            center = True
        if x > 500:
            if center:
                mask = np.zeros((200, 400))
                light_on += 1
                print(light_on)
                people_visited += 1
                mask = cv2.putText(mask, 'PEOPLE ENTERED = '+str(light_on), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255), 2)
                center = False
                left = False
            else:
                right = True
                left = False
    elif right:
        if x > 110 and x < 500 and not(center):
            center = True
        if x < 110:
            if center:
                mask = np.zeros((200, 400))
                if light_on > 0:
                   light_on -= 1
                people_left += 1
                print(light_on)
                mask = cv2.putText(mask, 'PEOPLE LEFT = '+str(light_on),  (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255), 2)
                center = False
                right = False
            else:
                left = True
                right = False

    people_in_shop = people_visited - people_left
    cv2.putText(frame1, 'IN-->',  (110, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255), 2)
    cv2.putText(frame1, '<--EXIT',  (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255), 2)
    cv2.putText(frame1, 'PEOPLE_IN_SHOP = '+str(people_in_shop),  (250, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(frame1, 'PEOPLE_LEFT = '+str(people_left),  (250, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    cv2.putText(frame1, 'PEOPLE_VISITED = '+str(people_visited),  (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)



    cv2.imshow("CAMERA", frame1)
    cv2.imshow('STATUS', mask)
    ret, frame1 = cap.read()
    if cv2.waitKey(1) == 27:
        break
cap.release()
