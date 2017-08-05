import cv2

img1 = cv2.imread('back.jpg')
img2 = cv2.imread('marco_desconocido.png')
dst = cv2.addWeighted(img1,1.0,img2,0.5,50)
cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
