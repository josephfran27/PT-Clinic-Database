import mysql.connector
from datetime import datetime, timedelta, date
import config 

# function for connecting to SQL database
def create_connection():
    try: 
        return mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# function to schedule an appointment
def schedule_appointment():
    print("APPOINTMENT SCHEDULING")
    print("Input required fields...")

    # inputs
    patient_id = int(input("Enter Patient ID: "))
    therapist_id = int(input("Enter Therapist ID: "))
    appointment_date = input("Enter Appointment Date (YYYY-MM-DD): ")
    appointment_time = input("Enter Appointment Time (HH:MM:SS): ")
    treat_plan_id = (input("Enter Treatment Plan ID (or Enter to skip): "))
    treat_plan_id = int(treat_plan_id) if treat_plan_id else None

    # connect to database
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    # verify that Patient ID exists
    cursor.execute("SELECT * FROM PATIENT WHERE Patient_id = %s", (patient_id,))
    if not cursor.fetchone():
        print("Error: Patient ID does not exist.")
        cursor.close()
        conn.close()
        return

    # verify that Therapist ID exists
    cursor.execute("SELECT * FROM THERAPIST WHERE Therapist_id = %s", (therapist_id,))
    if not cursor.fetchone():
        print("Error: Patient ID does not exist.")
        cursor.close()
        conn.close()
        return
    
    # verify that therapist is avaoilable at the given date and time
    cursor.execute("""
        SELECT * FROM APPOINTMENT 
        WHERE Therapist_id = %s AND Appointment_date = %s AND Appointment_time = %s
    """, (therapist_id, appointment_date, appointment_time))
    if cursor.fetchone():
        print("Error: Therapist is not available at the given date and time.")
        cursor.close()
        conn.close()
        return
    
    # insert appointment into APPOINTMENT table
    cursor.execute("""
        INSERT INTO APPOINTMENT (Patient_id, Therapist_id, Treat_plan_id, Appointment_date, Appointment_time, Appointment_status) 
        VALUES (%s, %s, %s, %s, %s, 'Scheduled')
    """, (patient_id, therapist_id, treat_plan_id, appointment_date, appointment_time))

    appointment_id = cursor.lastrowid  # get the last inserted appointment ID
    conn.commit()

    # retrieve and display details of the scheduled appointment
    cursor.execute("""
        SELECT
            a.Appointment_id,
            CONCAT(p.Fname, ' ', p.Lname) AS Patient,
            CONCAT(t.Fname, ' ', t.Lname) AS Therapist,
            a.Appointment_date,
            a.Appointment_time
        FROM APPOINTMENT a
        JOIN PATIENT p ON a.Patient_id = p.Patient_id
        JOIN THERAPIST t ON a.Therapist_id = t.Therapist_id
        WHERE a.Appointment_id = %s
    """, (appointment_id,))

    appointment = cursor.fetchone()

    # print information
    print(f"\nAppointment Scheduled Successfully!")
    print(f"Appointment ID: {appointment['Appointment_id']}")
    print(f"Patient: {appointment['Patient']}")
    print(f"Therapist: {appointment['Therapist']}")
    print(f"Date/Time: {appointment['Appointment_date']} at {appointment['Appointment_time']}")

    cursor.close()
    conn.close()

# function to create a treatment plan
def create_treatment_plan():
    print("TREATMENT PLAN CREATION")
    print("Input required fields...")

    # inputs 
    patient_id = int(input("Enter Patient ID: "))
    therapist_id = int(input("Enter Therapist ID: "))
    diagnosis = input("Enter Diagnosis: ")
    goals = input("Enter Goals: ")
    start_date = input("Enter Start Date (YYYY-MM-DD): ")
    end_date = input("Enter End Date (YYYY-MM-DD): ")

    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    # verify that Patient ID exists
    cursor.execute("SELECT * FROM PATIENT WHERE Patient_id = %s", (patient_id,))
    if not cursor.fetchone():
        print("Error: Patient ID does not exist.")
        cursor.close()
        conn.close()
        return
    
    # verify that Therapist ID exists
    cursor.execute("SELECT * FROM THERAPIST WHERE Therapist_id = %s", (therapist_id,))
    if not cursor.fetchone():
        print("Error: Therapist ID does not exist.")
        cursor.close()
        conn.close()
        return
    
    # insert treatment plan into TREATMENT_PLAN table
    cursor.execute("""
        INSERT INTO TREATMENT_PLAN (Goals, Diagnosis, Start_date, End_date, Patient_id, Therapist_id) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (goals, diagnosis, start_date, end_date, patient_id, therapist_id))

    plan_id = cursor.lastrowid
    conn.commit()

    # retrieve and display details of the scheduled appointment
    cursor.execute("""
        SELECT
            tp.Treat_plan_id,
            CONCAT(p.Fname, ' ', p.Lname) AS Patient,
            CONCAT(t.Fname, ' ', t.Lname) AS Therapist,
            tp.Diagnosis,
            tp.Goals,
            tp.Start_date,
            tp.End_date
        FROM TREATMENT_PLAN tp
        JOIN PATIENT p ON tp.Patient_id = p.Patient_id
        JOIN THERAPIST t ON tp.Therapist_id = t.Therapist_id
        WHERE tp.Treat_plan_id = %s
    """, (plan_id,))

    result = cursor.fetchone()

    # calculate duration in days
    days = (result['End_date'] - result['Start_date']).days

    # treatmend plan information
    print(f"\nTreatment Plan created successfully!")
    print(f"Treatment Plan ID: {result['Treat_plan_id']}")
    print(f"Patient: {result['Patient']}")
    print(f"Therapist: {result['Therapist']}")
    print(f"Diagnosis: {result['Diagnosis']}")
    print(f"Goals: {result['Goals']}")
    print(f"Duration: {days} days (from {result['Start_date']} to {result['End_date']})")

    cursor.close()
    conn.close()

def generate_billing():
    print("GENERATE BILLING")

    # start with showing unbilled appointments
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            a.Appointment_id,
            CONCAT(p.Fname, ' ', p.Lname) AS Patient,
            CONCAT(t.Fname, ' ', t.Lname) AS Therapist,
            a.Appointment_date,
            a.Appointment_status
        FROM APPOINTMENT a
        JOIN PATIENT p ON a.Patient_id = p.Patient_id
        JOIN THERAPIST t ON a.Therapist_id = t.Therapist_id
        WHERE a.Appointment_status = 'Completed'
        AND a.Appointment_id NOT IN (SELECT Appointment_id FROM BILLING)
    """)

    unbilled = cursor.fetchall()

    if unbilled:
        print("Unbilled Completed Appointments:")
        for row in unbilled:
            print(f"Appointment ID: {row['Appointment_id']}, Patient: {row['Patient']}, Therapist: {row['Therapist']}, Date: {row['Appointment_date']}")
    else:
        print("No unbilled completed appointments found.")
        cursor.close()
        conn.close()
        return

    print("Input required fields...")
    appointment_id = int(input("Enter Appointment ID: "))
    # default price will be $100 per session
    rate = float(input("Enter Rate per Session (default 100): ") or "100")

    # verify that Appointment ID exists
    cursor.execute("SELECT * FROM APPOINTMENT WHERE Appointment_id = %s", (appointment_id,))
    appt = cursor.fetchone()

    if not appt: 
        print("Error: Appointment ID does not exist.")
        cursor.close()
        conn.close()
        return

    # check that the appointment status is complete
    if appt['Appointment_status'] != 'Completed':
        print("Error: Billing can only be generated for completed appointments.")
        cursor.close()
        conn.close()
        return

    # check if billing already exists for this appointment
    cursor.execute("SELECT * FROM BILLING WHERE Appointment_id = %s", (appointment_id,))
    if cursor.fetchone():
        print("Error: Billing already exists for this appointment.")
        cursor.close()
        conn.close()
        return

    # create billing information
    patient_id = appt['Patient_id']
    billing_date = date.today()
    due_date = billing_date + timedelta(days=30)
    card_num = f"****{patient_id:04d}"  # dummy card number for illustration

    # insert billing into BILLING table
    cursor.execute("""
        INSERT INTO BILLING (Appointment_id, Patient_id, Billing_date, Billing_total, Card_num, Due_date)      
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (appointment_id, patient_id, billing_date, rate, card_num, due_date)) 
    
    billing_id = cursor.lastrowid
    conn.commit()

    # retrieve and display billing details
    cursor.execute("""
        SELECT
            b.Bill_id,
            CONCAT(p.Fname, ' ', p.Lname) AS Patient,
            p.Insurance_num,
            CONCAT(t.Fname, ' ', t.Lname) AS Therapist,
            a.Appointment_date,
            b.Billing_total,
            b.Due_date
        FROM BILLING b
        JOIN APPOINTMENT a ON b.Appointment_id = a.Appointment_id
        JOIN PATIENT p ON b.Patient_id = p.Patient_id
        JOIN THERAPIST t ON a.Therapist_id = t.Therapist_id
        WHERE b.Bill_id = %s
    """, (billing_id,))

    result = cursor.fetchone()

    # display
    print(f"\nBilling Invoice created successfully!")
    print(f"Patient: {result['Patient']}")
    print(f"Therapist: {result['Therapist']}")
    print(f"Appointment Date: {result['Appointment_date']}")
    print(f"Amount Due: ${result['Billing_total']}")
    print(f"Due Date: {result['Due_date']}")

    cursor.close()
    conn.close()

# main program
def main():
    while True:
        print("\nPHYSICAL THERAPY CLINIC MANAGEMENT SYSTEM")
        print("1. Schedule Appointment")
        print("2. Create Treatment Plan")
        print("3. Generate Billing")
        print("4. Quit")

        choice = input("Select an option: ")

        if choice == '1':
            schedule_appointment()
        elif choice == '2':
            create_treatment_plan()
        elif choice == '3':
            generate_billing()
        elif choice == '4':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Please enter a valid option.")

if __name__ == "__main__":
    main()

