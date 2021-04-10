import cv2
import numpy as np
import face_recognition
import time
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
import serial                                                              
import time                                                                  


video_capture=cv2.VideoCapture(0)

varun_image = face_recognition.load_image_file("varun.jpeg")
varun_face_encoding = face_recognition.face_encodings(varun_image)[0]

# sample picture and recognize it.
srija_image = face_recognition.load_image_file("srija.jpg")
srija_face_encoding = face_recognition.face_encodings(srija_image)[0]

# arrays of known face encodings and their names created
known_face_encodings = [
    varun_face_encoding,
    srija_face_encoding
]
known_face_names = [
    "varun",
    "Srija"
]

while True:
	ret,frame=video_capture.read()
	
	rgb_frame=frame[:,:,::-1]
	
	face_locations=face_recognition.face_locations(rgb_frame)
	face_encodings=face_recognition.face_encodings(rgb_frame,face_locations)
	
	name = "Unknown face"
	for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
		
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
		name = "Unknown face"

		if True in matches:
			first_match_index = matches.index(True)
			name = known_face_names[first_match_index]

		
		cv2.rectangle(frame,(left,bottom-35),(right,bottom),(0,0,255),cv2.FILLED)
		font=cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(frame,name,(left+6,bottom-6),font,1.0,(255,255,255),1)
		if name!="Unknown face":
			print(name,"was here")
			break
		else:
			print('face not recognized')
	
	cv2.imshow('Video',frame)
	
	if name!="Unknown face":
		#print(name,"was here")
		break
	
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video_capture.release()
cv2.destroyAllWindows()

#allowing time to wear the mask
print("please wear your mask")
time.sleep(3)



#arduino code


def door(var):
        
    
    ser = serial.Serial('/dev/ttyACM0',baudrate = 2400, timeout = 3)    
    print(ser.readline())
    while 1:         
                                                     
        if (var == 1):                                                       
            ser.write("1".encode())                            
            print ("person is wearing the mask")         
            return
            time.sleep(5)          
        if (var == 0):
            ser.write("0".encode())              
            print ("Please wear your mask") 
            return        
            time.sleep(5)




#mask code



if name in known_face_names:

    def detect_and_predict_mask(frame, faceNet, maskNet):
        

        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
            (104.0, 177.0, 123.0))

        # pass the blob through the network and obtain the face detections
        faceNet.setInput(blob)
        detections = faceNet.forward()
        #print(detections.shape)

        # initialize our list of faces, their corresponding locations,
        # and the list of predictions from our face mask network
        faces = []
        locs = []
        preds = []

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the detection
            confidence = detections[0, 0, i, 2]

            
            if confidence > 0.5:
                
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                
                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

                
                face = frame[startY:endY, startX:endX]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)

               
                faces.append(face)
                locs.append((startX, startY, endX, endY))

        # only make a predictions if at least one face was detected
        if len(faces) > 0:
           
            faces = np.array(faces, dtype="float32")
            preds = maskNet.predict(faces, batch_size=32)

        
        return (locs, preds)

    
    prototxtPath = r"./deploy.prototxt"
    weightsPath = r"./res10_300x300_ssd_iter_140000.caffemodel"
    faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

  
    maskNet = load_model("mask_detector.model")

    # initialize the video stream
    print("starting video stream...")
    #url = "http://192.168.43.1:8080/video"
    vs = VideoStream(0).start()


    # loop over the frames from the video stream
    while True:
        
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
        
        # loop over the detected face locations and their corresponding
        # locations
        for (box, pred) in zip(locs, preds):
            
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred
            
            
            door(1) if mask > withoutMask else door(0)
            time.sleep(3)
            
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            
            cv2.putText(frame, label, (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
       


	
