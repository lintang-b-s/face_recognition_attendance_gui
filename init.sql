
use attendance;

drop table if exists attendance;

drop table if exists meeting;
drop table  if exists teaches;
drop table if exists takes;


drop table if exists section;
drop table if exists course;
drop table if exists classroom;
drop table if exists instructor;

drop table if exists student;

create table course
(
  course_id  varchar(10),
  title varchar(255),
  dept_name varchar(255),
  sks numeric(2,0) check (sks > 0),
  primary key (course_id)
);


create table classroom 
(
  building varchar(255),
  room_number varchar(255),
  capacity numeric(4,0) check (capacity >0),
  primary key (building, room_number)
);

create table instructor
(
  instructor_id varchar(10),
  name varchar(255),
  dept_name varchar(255),
  primary key (instructor_id)
);

create table section
(
  course_id varchar(10),
  sec_id varchar(10),
  semester varchar(10),
  year numeric(4),
  building varchar(255),
  room_number varchar(255),
  day varchar(50),
  start_hr numeric(2),
  start_min numeric(2),
  end_hr numeric(2),
  end_min numeric(2),
  primary key (course_id, sec_id, semester, year),
  foreign key (course_id) references course (course_id) on delete cascade,
  foreign key (building, room_number) references classroom (building, room_number) on delete cascade
);



create table teaches 
(
  instructor_id varchar(10),
  course_id  varchar(10),
  sec_id varchar(10),
  semester varchar(10),
  year numeric(4),
  primary key (instructor_id, course_id, sec_id, semester, year),
  foreign key (course_id, sec_id, semester, year) references section(course_id, sec_id, semester, year) on delete cascade,
  foreign key (instructor_id) references instructor(instructor_id) on delete cascade

);


create table student 
(
  nim varchar(100),
  name varchar(255),
  address varchar(255),
  email varchar(255),
  primary key (nim)
);

create table takes 
(
  nim varchar(100),
  course_id varchar(10),
  sec_id varchar(10),
  semester varchar(10),
  year numeric(4,0),
  primary key (nim, course_id, sec_id, semester, year),
  foreign key (course_id, sec_id, semester, year) references section(course_id, sec_id, semester, year) on delete cascade,
  foreign key (nim) references student(nim) on delete cascade
);


create table meeting
(
  -- meeting_id int(11) not null auto_increment,
  course_id varchar(10),
  sec_id varchar(10),
  semester varchar(10),
  year numeric(4,0),
  meeting_num numeric(2),
  meeting_date date,
  start_hour datetime,
  end_hour datetime,
  room varchar(255),
  primary key (course_id, sec_id, semester, year, meeting_num, meeting_date, start_hour, end_hour, room),
  foreign key (course_id, sec_id, semester, year) references section(course_id, sec_id, semester, year) on delete cascade
);


create table attendance
(
  attendance_id int(11) not null auto_increment,
  nim varchar(100),
  student_name varchar(255),
  instructor_id varchar(10),
  course_id varchar(10),
  sec_id varchar(10),
  semester varchar(10),
  year numeric(4,0),
  meeting_num numeric(2),
  meeting_date date,
  start_hour datetime,
  end_hour datetime,
  room varchar(255),
  present_hour datetime,
  notes varchar(255),
  aStatus varchar(255),
  primary key (attendance_id),
  foreign key (course_id, sec_id, semester, year, meeting_num, meeting_date, start_hour, end_hour, room) references  meeting (course_id, sec_id, semester, year, meeting_num, meeting_date, start_hour, end_hour, room) on delete cascade,
  foreign key (nim) references student(nim) on delete cascade,
  foreign key (instructor_id) references instructor(instructor_id) on delete cascade
);




insert into course(course_id, title, dept_name, sks) values("123", "IOT", "DIKE", 3.0);
insert into classroom(building, room_number, capacity) values("FMIPA", "R.305", 60);
insert into instructor(instructor_id, name, dept_name) values("123", "Sri Mulyana phd", "DIKE");
insert into section(course_id, sec_id, semester, year, building, room_number, day, start_hr, start_min, end_hr, end_min) values("123", "123", "Ganjil/3", 2023, "FMIPA", "R.305", "selasa", 9, 10, 12, 10);
insert into teaches(instructor_id, course_id, sec_id, semester, year) values("123", "123","123",  "Ganjil/3", 2023);
insert into student(nim, name, address, email) values("123", "lintangbirdasaputra", "pogung", "a@gmail.com");
insert into takes(nim, course_id, sec_id, semester, year) values("123", "123", "123",  "Ganjil/3", 2023);
insert into meeting(course_id, sec_id, semester, year, meeting_num, meeting_date, start_hour, end_hour, room ) values("123", "123", "Ganjil/3", 2023, "1", "2023-08-23", "2023-08-23 09:00:00", "2023-08-23 15:00:00", "R.305"  );

