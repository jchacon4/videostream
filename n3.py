import cv2
import numpy as np
import imutils
import face_recognition
import datetime
import time

# setup initial location of window

video_capture = cv2.VideoCapture(0)
img2 = cv2.imread('negronegro.png')
img1 = cv2.imread('conocido.png')
 # Crop from x, y, w, h -> 100, 200, 300, 400

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
jc_image = face_recognition.load_image_file("jc.png")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
jc_face_encoding = face_recognition.face_encodings(jc_image)[0]


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


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

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces([obama_face_encoding, jc_face_encoding], face_encoding)
            name = "Unknown"
            conoce = False

            if match[0]:
                name = "Barack"
                conoce = True
            if match[1]:
                name = "JC"
                conoce = True

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
        cv2.putText(frame, ts, (43, 104), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        # Draw a label with a name below the face
        #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        #font = cv2.FONT_HERSHEY_DUPLEX
        #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


    if not conoce:
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

    if conoce:
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





    cv2.imshow('hola',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
