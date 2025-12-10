# Physical Therapy Clinic Management System

This application is a final project for a database class. It manages a physical therapy clinic mock database, supporting three main functions.
1. **Schedule Patient Appointments** - Book appointments with therapist availability checking
2. **Create Treatment Plans** - Assign treatment plans to patients with specific goals
3. **Generate Billing** - Create invoices for completed appointments

## Setup Instructions

### 1. Install MySQL Connector

```bash
pip install mysql-connector-python
```

### 2. Configure Database Connection

Update `config.py` with your MySQL credentials:

```python
DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASSWORD = 'your_password_here'  # UPDATE THIS
DB_NAME = 'pt_clinic'
```

### 3. Create Database and Tables

Open MySQL and run your schema file:

```bash
mysql -u root -p
```

Then:

```sql
SOURCE /path/to/schema.sql;
```

Or copy/paste the schema.sql contents into MySQL.

### 4. Populate Database with Sample Data

```bash
mysql -u root -p pt_clinic < sample_data.sql
```

Or in MySQL:

```sql
USE pt_clinic;
SOURCE /path/to/sample_data.sql;
```

### 5. Run the Application

```bash
python3 clinic.py
```

---
## Future Goals

I plan on creating front end using Streamlit.