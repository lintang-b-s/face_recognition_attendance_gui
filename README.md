# face_recognition_attendance_gui

## Quick Start

```
paste your photo in the 'muka' folder and rename the photo file with your name
```


### test face recognition without mysql

```
python pengenalanRai.py
```


```
press 'q' to quit 
```



### test with mysql

```
```

```
execute init.sql in mysql workbench
```

```
insert all student data in student table with the same name as the names of all the photos in the  'muka' directory
```


```
insert course,student, takes,section, meeting, course. example:


insert into course(course_id, title, dept_name, sks) values("123", "IOT", "DIKE", 3.0);
insert into classroom(building, room_number, capacity) values("FMIPA", "R.305", 60);
insert into section(course_id, sec_id, semester, year, building, room_number, day, start_hr, start_min, end_hr, end_min) values("123", "123", "Ganjil/3", 2023, "FMIPA", "R.305", "selasa", 9, 10, 12, 10);
insert into student(nim, name, address, email) values("123", "lintangbirdasaputra", "pogung", "a@gmail.com");
insert into takes(nim, course_id, sec_id, semester, year) values("123", "123", "123",  "Ganjil/3", 2023);
insert into meeting(course_id, sec_id, semester, year, meeting_num, meeting_date, start_hour, end_hour, room ) values("123", "123", "Ganjil/3", 2023, "1", "2023-08-23", "2023-08-23 09:00:00", "2023-08-23 15:00:00", "R.305"  );


notes: name in student must match with photo name
notes: meeting start_hour and end_hour must match with the time when you test the application
notes: meeting course being tested must match the course you are taking (takes table)


```

```
python pengenalanRaiMysql.py
```


```
press 'q' to quit 
```


## ER Diagram
![alt text](https://res.cloudinary.com/tutorial-lntng/image/upload/v1692772060/EERDIAGRAMSMARTCLASSROOM_li9pr0.png)


### To Do:
1. Connect to mysql
2. Tkinter GUI
3. Raspberry Pi
4. fix an error if face was not registered


### Test
![alt text](https://res.cloudinary.com/tutorial-lntng/image/upload/v1692699512/Screenshot_2023-08-22_at_16.58.29_ljsdge.png)

https://res.cloudinary.com/tutorial-lntng/image/upload/v1692699512/Screenshot_2023-08-22_at_16.58.29_ljsdge.png

![alt text](https://res.cloudinary.com/tutorial-lntng/image/upload/v1692774225/Screenshot_2023-08-23_at_14.02.59_tlsm1v.png)