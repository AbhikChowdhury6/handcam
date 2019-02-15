import cv2


cap = cv2.VideoCapture("http://192.168.43.209:12345/")


while(True):
    ret, frame = cap.read()
    print(ret)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()