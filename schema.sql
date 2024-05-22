DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS jobs;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  hash TEXT NOT NULL
);

CREATE TABLE doctors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  title TEXT,
  professional_license TEXT,
  phone TEXT,
  e_mail TEXT,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER,
    first_name  TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    face_shape TEXT,
    basic_color TEXT,
    colorimeter TEXT,
    gum_color TEXT,
    FOREIGN KEY (doctor_id) REFERENCES doctors (id)
);

CREATE TABLE jobs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  patient_id INTEGER,
  teeth TEXT NOT NULL,
  tooth_type TEXT,
  job_type TEXT,
  job_material TEXT,
  job_option TEXT,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  comments TEXT,
  status TEXT,
  FOREIGN KEY (patient_id) REFERENCES patients (id)
);



CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
