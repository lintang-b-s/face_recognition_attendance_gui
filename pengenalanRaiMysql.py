#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 07:24:37 2023

@author: lintangbirdasaputra
"""

import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pickle
import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error
import random




try:
    connection =  connect(
        host="localhost",
        user= "root",
        password= "12345678",
        database = "attendance"
    )
    print(connection)
except Error as e:
    print(e)
# else:
  
sqlCursor = connection.cursor()

path = 'muka'

images = []
classNames = []
mylist = os.listdir(path)
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList
encoded_face_train = findEncodings(images)

selectMeetingNow = "SELECT * FROM meeting WHERE CAST(NOW() AS TIME) BETWEEN CAST(meeting.start_hour AS TIME) AND CAST(meeting.end_hour AS TIME)"
getNim =( "SELECT nim FROM student where name=%s")
insertToAttendance = ( "INSERT INTO attendance(nim, student_name , course_id, sec_id, semester, year, meeting_num, meeting_date, start_hour, end_hour, room, present_hour) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
getCourseSectionTakes = ("SELECT * FROM takes WHERE nim=%s AND course_id=%s AND sec_id=%s AND semester=%s AND year=%s")
getStudentAttendance = ("SELECT * FROM attendance WHERE nim=%s AND meeting_num=%s AND meeting_date=%s AND start_hour=%s AND end_hour=%s AND room=%s AND course_id=%s AND sec_id=%s AND semester=%s AND year=%s ")



def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            time = now.strftime('%I:%M:%S:%p')
            date = now.strftime('%d-%B-%Y')
            f.writelines(f'n{name}, {time}, {date}')
            
            

# take pictures from webcam 
cap  = cv2.VideoCapture(0)
while True:
    sqlCursor.execute(selectMeetingNow)
    resultMeeting=   sqlCursor.fetchone()
   

    courseId = resultMeeting[0]
    secId  = resultMeeting[1]
    semester=  resultMeeting[2]
    year  = resultMeeting[3]
    meetingNum = resultMeeting[4]
    meetingDate = resultMeeting[5]
    startHour =  resultMeeting[6]
    endHour = resultMeeting[7]
    room =  resultMeeting[8]
    
    randomNim = str(random.random())
    # 15  kolom
    

    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faces_in_frame = face_recognition.face_locations(imgS)
    encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
    for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
        matches = face_recognition.compare_faces(encoded_face_train, encode_face)
        faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
        matchIndex = np.argmin(faceDist)
        # print(matchIndex)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper().lower()
            y1,x2,y2,x1 = faceloc
            # since we scaled down by 4 times
            y1, x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img, (x1,y2-35),(x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img,name, (x1+6,y2-5), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
          
            
            # getName           
            sqlCursor.execute(getNim, (name,) )
            nim = sqlCursor.fetchone()

            # resultMeeting
            # check if user take the course section or not
            sqlCursor.execute(getCourseSectionTakes, (nim[0], courseId, secId, semester, year))
            isStudentTakeCourseSection = sqlCursor.fetchone()
            if (isStudentTakeCourseSection == None):
                continue
            
            
            
            # check if user already absen 
            sqlCursor.execute(getStudentAttendance, (nim[0], meetingNum, meetingDate, startHour, endHour, room, courseId, secId, semester, year))
            isStudentAlreadyAbsenInTheClass = sqlCursor.fetchone()
            if (isStudentAlreadyAbsenInTheClass != None):
                continue
            
            
            # add attendance data in db
            inserted = sqlCursor.execute(insertToAttendance,( nim[0],name, courseId,  secId, semester, year, meetingNum, meetingDate,   startHour,  endHour, room,  datetime.now()) )
            # commit insert statement
            connection.commit()
        # else: 
        #     continue
    cv2.imshow('webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
# close mysql
connection.close()