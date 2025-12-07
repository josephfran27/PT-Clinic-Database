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
    print(f"Appointment Scheduled Successfully!")
    print(f"Appointment ID: {appointment['Appointment_id']}")
    print(f"Patient: {appointment['Patient']}")
    print(f"Therapist: {appointment['Therapist']}")
    print(f"Date/Time: {appointment['Appointment_date']} at {appointment['Appointment_time']}")

    cursor.close()
    conn.close()

def main():
    while True:
        print("Physical Therapy Clinic Management System")
        print("1. Schedule Appointment")
        print("4. Quit")

        choice = input("Select an option: ")

        if choice == '1':
            schedule_appointment()
        elif choice == '4':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Please enter a valid option.")

if __name__ == "__main__":
    main()







