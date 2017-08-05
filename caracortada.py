import cv2
import numpy as np
import imutils
import face_recognition
import datetime
import time
from PIL import Image
from random import randint
from kairos import register, recognize, verify
from up import upload

# setup initial location of window

video_capture = cv2.VideoCapture(0)
#time.sleep(1)
img2 = cv2.imread('desconocido.png')
img1 = cv2.imread('conocido.png')
black = cv2.imread('black.jpg')
cuadro = cv2.imread('cuadro_negro_conpiquito.png')

# Load a sample picture and learn how to recognize it.
jc_image = face_recognition.load_image_file("jc.png")
jc_face_encoding = face_recognition.face_encodings(jc_image)[0]


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
unknow_count = 0
process_this_frame = True
caritas = [jc_face_encoding]
nadie = False

gen = randint(0, 5000)




def getdatos(imagen, who, gallery):
    subir = upload(imagen)
    print(subir)
    registro = register(subir, who, gallery)
    edad = int(registro['images'][0]['attributes']['age'])
    sexo = registro['images'][0]['attributes']['gender']['type']
    datos = {'edad': edad, 'sexo': sexo}
    return(datos)
    #return registro


datos = getdatos("jc.png", "JC", "FiestaTejas")



def getFace(face_location, frame):
    top, right, bottom, left = face_location
    face_image = frame[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.save('13.jpg')
    why()


def why():
    carita_image = face_recognition.load_image_file('13.jpg')
    carita_face_encoding = face_recognition.face_encodings(carita_image)[0]
    results = face_recognition.compare_faces(caritas, carita_face_encoding)
    if not True in results:
        caritas.append(carita_face_encoding)
        unknow_count = 0
    else:
        unknow_count = 0




while True:
    ret, frame = video_capture.read()
    width = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    height = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)

    frame = frame[0:720,426:852]
    rows,cols,channels = img2.shape
    roi = frame[0:rows, 0:cols ]

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        if len(face_locations) == 0:
            nadie = True
        else:
            nadie = False

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(caritas, face_encoding)
            name = "Unknown"
            conoce = False


            if match[0]:
                name = "JC"
                conoce = True
            if not True in match:
                conoce = False
                if unknow_count == 0:
                    unknow_count = 1
                    for face_location in face_locations:
                        getFace(face_location, small_frame)



            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        if not conoce:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 8)
        else:
            cv2.rectangle(frame, (left, top), (right, bottom), (198, 123, 5), 8)


        # draw the timestamp on the frame
        timestamp = datetime.datetime.now()
        ts = timestamp.strftime("%d/%m/%y %I:%M:%S%p")
        cv2.putText(frame, ts, (43, 111), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        # Draw a label with a name below the face
        #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        #font = cv2.FONT_HERSHEY_DUPLEX
        #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


    if nadie:

        frame = black

    if not nadie and not conoce:
        # Now create a mask of logo and create its inverse mask also
        img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
        # Take only region of logo from logo image.
        img2_fg = cv2.bitwise_and(img2,img2,mask = mask)
        # Put logo in ROI and modify the main image
        dst = cv2.add(img1_bg,img2_fg)
        frame[0:rows, 0:cols ] = dst

    if not nadie and conoce:
        # Now create a mask of logo and create its inverse mask also
        img2gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
        # Take only region of logo from logo image.
        img2_fg = cv2.bitwise_and(img1,img1,mask = mask)
        # Put logo in ROI and modify the main image
        dst = cv2.add(img1_bg,img2_fg)
        frame[0:rows, 0:cols ] = dst

    img2gray = cv2.cvtColor(cuadro,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(cuadro,cuadro,mask = mask)
    # Put logo in ROI and modify the main image
    dst = cv2.add(img1_bg,img2_fg)
    frame[0:rows, 0:cols ] = dst

    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%I:%M:%S %p")
    sexo = datos['sexo']
    if sexo == "M":
        sexo = "Masculino"
    else:
        sexo = "Femenino"

    edad = datos['edad']
    edad = str(edad) + " Años"

    cv2.putText(frame, ts, (238, 567), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, sexo, (238, 514), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, edad,'utf-8',(238, 484), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)




    cv2.imshow('hola',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
