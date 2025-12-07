-- Physical Therapy Clinic Database: Joseph France

CREATE DATABASE IF NOT EXISTS pt_clinic;
USE pt_clinic;

-- For running multiple queries
DROP TABLE IF EXISTS SESSION_NOTES;
DROP TABLE IF EXISTS MEDICAL_CONDITIONS;
DROP TABLE IF EXISTS BILLING;
DROP TABLE IF EXISTS APPOINTMENT;
DROP TABLE IF EXISTS TREATMENT_PLAN;
DROP TABLE IF EXISTS THERAPIST;
DROP TABLE IF EXISTS PATIENT;

-- PATIENT table 
CREATE TABLE PATIENT (
	Patient_id INT PRIMARY KEY AUTO_INCREMENT, -- auto generate a num
	Fname VARCHAR(50) NOT NULL,
    Lname VARCHAR(50) NOT NULL,
    Insurance_num VARCHAR(50) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Street VARCHAR(50),
    City VARCHAR(50),
    Zip VARCHAR(5)
);

-- THERAPIST table
CREATE TABLE THERAPIST (
	Therapist_id INT PRIMARY KEY AUTO_INCREMENT,
    Fname VARCHAR(50) NOT NULL,
    Lname VARCHAR(50) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Hire_date DATE NOT NULL
);

-- TREATMENT_PLAN table
CREATE TABLE TREATMENT_PLAN (
	Treat_plan_id INT PRIMARY KEY AUTO_INCREMENT,
    GOALS TEXT,
    Diagnosis TEXT NOT NULL,
    Start_date DATE NOT NULL,
    End_date DATE NOT NULL,
    Patient_id INT NOT NULL,
    Therapist_id INT NOT NULL,
	-- when deleting patient, treatment plan is deleted 
    FOREIGN KEY (Patient_id) REFERENCES PATIENT(Patient_id) ON DELETE CASCADE,
	-- when deleting therapist, therapist, treatment plan remains but Therapist_id becomes NULL 
    FOREIGN KEY (Therapist_id) REFERENCES THERAPIST(Therapist_id) ON DELETE CASCADE
);

-- APPOINTMENT table
CREATE TABLE APPOINTMENT (
	Appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    Patient_id INT NOT NULL,
    Therapist_id INT NOT NULL,
    Treat_plan_id INT NOT NULL,
    Appointment_date DATE NOT NULL,
    Appointment_time TIME NOT NULL,
    Appointment_status VARCHAR(30) NOT NULL,
    -- when deleting patient, appointment(s) with the patient are deleted
    FOREIGN KEY (Patient_id) REFERENCES PATIENT(Patient_id) ON DELETE CASCADE,
    -- when deleting therapist, appointment(s) under that therapist are deleted
    FOREIGN KEY (Therapist_id) REFERENCES THERAPIST(Therapist_id) ON DELETE CASCADE,
    -- when deleting treatment plan, appointments with that plan are deleted
    FOREIGN KEY (Treat_plan_id) REFERENCES TREATMENT_PLAN(Treat_plan_id) ON DELETE CASCADE
);

-- BILLING table
CREATE TABLE BILLING (
	Bill_id INT PRIMARY KEY AUTO_INCREMENT,
    Appointment_id INT NOT NULL,
    Patient_id INT NOT NULL,
    Billing_date DATE NOT NULL,
    Billing_total DECIMAL(10, 2) NOT NULL,
    Card_num VARCHAR(20) NOT NULL,
    Due_date DATE NOT NULL,
    -- when deleting appointment, delete billing info 
    FOREIGN KEY (Appointment_id) REFERENCES APPOINTMENT(Appointment_id) ON DELETE CASCADE,
    -- when deleting patients, delete billing info 
    FOREIGN KEY (Patient_id) REFERENCES PATIENT(Patient_id) ON DELETE CASCADE
);

-- SESSION_NOTES table
CREATE TABLE SESSION_NOTES (
	Session_num INT NOT NULL,
    Appointment_id INT NOT NULL,
    Session_date DATE NOT NULL,
    Progress TEXT,
    Notes TEXT,
    -- composite primary key
    PRIMARY KEY (Appointment_id, Session_num),
    -- when deleting appointments, delete session notes too
    FOREIGN KEY (Appointment_id) REFERENCES APPOINTMENT(Appointment_id) ON DELETE CASCADE
);

-- MEDICAL_CONDITIONS table
CREATE TABLE MEDICAL_CONDITIONS (
	Patient_id INT NOT NULL,
    Medical_condition VARCHAR(100) NOT NULL,
    PRIMARY KEY (Patient_id, Medical_condition),
    FOREIGN KEY (Patient_id) REFERENCES PATIENT(Patient_id) ON DELETE CASCADE
);

