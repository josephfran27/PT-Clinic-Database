USE pt_clinic;

-- insert patients
INSERT INTO PATIENT (Fname, Lname, Insurance_num, Phone, Street, City, Zip) VALUES 
('Joseph', 'France', 'HLTH1265', '573-555-1234', '123 Apple St', 'Columbia', '65201'),
('Sarah', 'Jackson', 'HLTH3927', '573-555-2387', '456 Orange Rd', 'Columbia', '65202'),
('Micheal', 'Johnson', 'HLTH1029', '573-555-2357', '789 Grape Ln', 'Columbia', '65201'),
('William', 'Hunt', 'HLTH7812', '573-555-9612', '611 Banana Ave', 'Columbia', '65201'),
('Christoper', 'Talbot', 'HLTH0322', '573-555-1254', '521 Cranberry St', 'Columbia', '65205'),
('Sally', 'Simpson', 'HLTH4502', '573-555-8924', '243 Peach Rd', 'Columbia', '65203');

-- insert therapists
INSERT INTO THERAPIST (Fname, Lname, Phone, Hire_date) VALUES
('Dr Aidan', 'Brown', '573-555-2981', '2020-10-05'),
('Dr Sarah', 'Gettinger', '573-555-2982', '2020-05-13'),
('Dr Matthew', 'Summit', '573-555-7826', '2022-06-24');

-- insert treatment plans
INSERT INTO TREATMENT_PLAN (Goals, Diagnosis, Start_date, End_date, Patient_id, Therapist_id) VALUES
('Improve knee mobility, reduce pain', 'ACL tear recovery', '2024-11-01', '2025-02-01', 1, 1),
('Restore shoulder range of motion', 'Rotator cuff injury', '2024-11-05', '2025-01-05', 2, 2),
('Strengthen lower back, improve posture', 'Chronic lower back pain', '2024-11-10', '2025-03-10', 3, 1),
('Regain ankle stability', 'Ankle sprain', '2024-11-15', '2024-12-15', 4, 3),
('Improve hip flexibility', 'Hip bursitis', '2024-11-20', '2025-01-20', 5, 2);

-- insert appointments 
INSERT INTO APPOINTMENT (Patient_id, Therapist_id, Treat_plan_id, Appointment_date, Appointment_time, Appointment_status) VALUES
(1, 1, 1, '2024-11-25', '09:00:00', 'Completed'),
(1, 1, 1, '2024-11-27', '09:00:00', 'Completed'),
(2, 2, 2, '2024-11-26', '10:00:00', 'Completed'),
(3, 1, 3, '2024-11-28', '14:00:00', 'Completed'),
(4, 3, 4, '2024-12-06', '11:00:00', 'Scheduled'),
(5, 2, 5, '2024-12-09', '15:00:00', 'Scheduled'),
(1, 1, 1, '2024-12-11', '09:00:00', 'Scheduled');

-- insert billing info
INSERT INTO BILLING (Appointment_id, Patient_id, Billing_date, Billing_total, Card_num, Due_date) VALUES
(1, 1, '2024-11-25', 150.00, '1234', '2024-12-25'),
(2, 1, '2024-11-27', 150.00, '1234', '2024-12-27'),
(3, 2, '2024-11-26', 150.00, '5678', '2024-12-26'),
(4, 3, '2024-11-28', 150.00, '9012', '2024-12-28');


-- insert session notes
INSERT INTO SESSION_NOTES (Appointment_id, Session_num, Session_date, Progress, Notes) VALUES 
(1, 1, '2024-11-25', 'Baseline established', 'Patient shows good motivation. Range of motion at 60%.'),
(2, 2, '2024-11-27', 'Improving steadily', 'Range of motion increased to 70%. Reduced pain reported.'),
(3, 1, '2024-11-26', 'Good initial progress', 'Shoulder elevation improved by 15 degrees.'),
(4, 1, '2024-11-28', 'Core strengthening started', 'Patient responded well to exercises.');



-- insert medical conditions
INSERT INTO MEDICAL_CONDITIONS (Patient_id, Medical_condition) VALUES 
(1, 'Low back pain'),
(2, 'Shoulder impingement syndrome'),
(3, 'Carpal tunnel syndrome'),
(4, 'Achilles tendinopathy'),
(5, 'Meniscus tear'),
(6, 'Plantar fasciitis');