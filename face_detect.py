import cv2
import numpy as np
import face_recognition
import time

video_capture=cv2.VideoCapture(0)

varun_image = face_recognition.load_image_file("varun.jpeg")
varun_face_encoding = face_recognition.face_encodings(varun_image)[0]

# sample picture and recognize it.
srija_image = face_recognition.load_image_file("srija.jpg")
srija_face_encoding = face_recognition.face_encodings(srija_image)[0]

#arrays created of known faces
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
			print('Face found',name)
		
		else:
			print('face not recognized')
	
	cv2.imshow('Video',frame)
	
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video_capture.release()
cv2.destroyAllWindows()

