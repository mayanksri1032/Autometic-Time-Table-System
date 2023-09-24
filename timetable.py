import mysql.connector as sql
import random
from prettytable import PrettyTable

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "101134",
    "database": "lnct"
}

# Function to generate a class-wise timetable
def generate_timetable():
    try:
        conn = sql.connect(**db_config)
        cursor = conn.cursor()

        # Fetch teachers, classes, and subjects from the database
        cursor.execute("SELECT teacher_id, teacher_name FROM teachers")
        teachers = cursor.fetchall()

        cursor.execute("SELECT class_id, class_name FROM classes")
        classes = cursor.fetchall()

        cursor.execute("SELECT subject_id, subject_name FROM subjects")
        subjects = cursor.fetchall()

        # Define days and periods
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        periods_per_day = 6  # 6 periods per day

        # Create a PrettyTable for the timetable
        timetable = PrettyTable()
        timetable.field_names = ["Class"] + days

        # Create dictionaries to track assigned subjects by class
        class_subject_assignments = {class_name: {} for _, class_name in classes}

        # Generate and add rows to the timetable
        for class_id, class_name in classes:
            row_data = [class_name]
            for day in days:
                subjects_assigned = []
                for period in range(1, periods_per_day + 1):
                    # Ensure that each subject is assigned only once to a class
                    available_subjects = [s for s in subjects if s[0] not in class_subject_assignments[class_name].values()]

                    if not available_subjects:
                        # If all subjects are assigned to this class, skip this period
                        subjects_assigned.append("N/A")
                    else:
                        subject_id, subject_name = random.choice(available_subjects)
                        class_subject_assignments[class_name][period] = subject_id
                        subjects_assigned.append(subject_name)

                row_data.append("\n".join(subjects_assigned))

            timetable.add_row(row_data)

        print(timetable)

        conn.commit()
    except sql.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Generate the class-wise timetable
generate_timetable()


