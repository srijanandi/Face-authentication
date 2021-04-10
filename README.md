# Face-authentication
Facial recognition is a personal identification system that uses personal characteristics of a person to identify the person's identity. This is one of the easiest ways to distinguish the individual identity. .Before giving entry, mask will be recognised. Temperature will be check. Sanitizer will be dispensed.
# Requirements
##Libraries : 
Face recognition
open cv
numpy
imutils
keras
tensorflow
time
pyserial

##Hardware:
arduino
LCD
Temperature sensor
motion detector
jumper wires


# How to run code
1. This repository consists of all resources except the datasets of mask and without mask (as it was large and couldn't be uploaded).
2. face_detect.py file detects the face of a person if it matches from the database
3. detect_mask.py file detects if the person is wearing mask or not.
4. arduino_connection.io is the code to be embedded on arduino.
5. combined.py file is the integration of our entire model. (will run when hardware is connected).
