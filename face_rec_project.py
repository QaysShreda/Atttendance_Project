from attr import attr
import face_recognition
import cv2
import numpy as np
from datetime import date
import json
from datetime import datetime
import requests



# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


# Load a sample picture and learn how to recognize it.
Adam_image = face_recognition.load_image_file("Adam_resized.jpg")
Adam_face_encoding = face_recognition.face_encodings(Adam_image)[0]

# Load a second sample picture and learn how to recognize it.
Alma_image = face_recognition.load_image_file("Alma_resized.jpg")
Alma_face_encoding = face_recognition.face_encodings(Alma_image)[0]

# Create arrays of known face encodings and their names
Monther_image = face_recognition.load_image_file("Monther_resized.jpg")
Monther_face_encoding = face_recognition.face_encodings(Monther_image)[0]

Yahya_image = face_recognition.load_image_file("Yahya_resized.jpg")
Yahya_face_encoding = face_recognition.face_encodings(Yahya_image)[0]


known_face_encodings = [
    Adam_face_encoding,
    Alma_face_encoding,
    Monther_face_encoding,
    Yahya_face_encoding
   
]
known_face_names = [
    "Adam",
    "Alma",
    "Monther",
    "Yahya"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
attendances = []
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                current_date = str(date.today())
                current_attendance = name
                print(current_attendance)

                if current_attendance not in attendances:
                    print("Add new student")
                    attendances.append(current_attendance)
                    r = requests.post('https://attendance-raspberry.herokuapp.com/', data=json.dumps({'name':current_attendance,'date':str(datetime.now())}))
                    print(r.text)
                    print(attendances)
                    print("Add new Student")
                else:
                    print(" Student Registerd ..")
        
            face_names.append(name)

    process_this_frame = not process_this_frame

    #name="No one"
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
    # Display the resulting image
    
    #print(name)
    #if name not in attendance_std:
    #current_attendance = [name,str(date.today())]


    
    cv2.imshow('Video', frame)
    ##cv2.imshow('Video', frame)
    #print(attendance_std)
   # else:
    #    cv2.imshow('Video', frame)
          #  print(name)
       
    
        
    
    #print(attendance_std)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

#print(attendance_std)
''''
att_lst=[[]]
std_date=["",""]

for i in range(0,len(attendance_std)-1):

    if attendance_std[i] == std_date[0] and std_date[1]==today:
        continue

    else:
        
        std_date[0]=(attendance_std[i])
        std_date[1]=today
        print(std_date)
         
        if std_date not in att_lst:
            att_lst.append(std_date)
            print("appended")
            print(att_lst)
    
#print(attendance_std)   
'''
