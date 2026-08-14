from student import Student, StudentManager
import pandas as pd
import numpy as np
from config import CSV_COLUMNS, PASSING_MARKS
from excel_export import export_to_excel
import matplotlib.pyplot as plt
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from datetime import datetime
student_file = ""
manager = StudentManager()
students = manager.get_students()

def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "Fail"
    students = []

while True:

    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1️⃣ Create New Student List")
    print("2️⃣ Open Existing Student List")
    print("3️⃣ Add Student")
    print("4️⃣ View Student")
    print("5️⃣ Search Student")
    print("6️⃣ Update Student")
    print("7️⃣ Delete Student")
    print("8️⃣ Student Statistics")
    print("9️⃣ Subject Statistics")
    print("🔟 Graphs")
    print("1️⃣1️⃣Export Current List to Excel ")
    print("1️⃣2️⃣ Export Current List to PDF")  
    print("1️⃣3️⃣Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        list_name = input("📁 Enter new student list name: ").strip()

        if list_name == "":
            print("❌ List name cannot be empty.")
            continue

        student_file = list_name + ".csv"

        students = []
        manager = StudentManager()

        try:
            df = pd.DataFrame(columns=CSV_COLUMNS)
            df.to_csv(student_file, index=False)
            print(f"✅ '{student_file}' created successfully!")

        except Exception as e:
            print(f"❌ Could not create '{student_file}'.")
            print(f"Reason: {e}")
            continue

    elif choice == "2":
        csv_files = []

        for file in os.listdir():
            if file.endswith(".csv"):
                csv_files.append(file)


        if len(csv_files) == 0:
            print("❌ No student lists available.")
            continue

        print("📂 Available Student Lists:")

        for i, file in enumerate(csv_files, 1):
            print(f"{i}. {file}")

        try:
            select = int(input("Enter list number: "))

        except ValueError:
            print("❌ Please enter a valid number.")
            continue

        if select < 1 or select > len(csv_files):
            print("❌ Invalid list number.")
            continue

        student_file = csv_files[select - 1]

        try:
            df = pd.read_csv(student_file)

            required_columns = CSV_COLUMNS

            if list(df.columns) != required_columns:
                print("❌ Invalid student CSV file.")
                print("Required columns:", required_columns)
                continue

            students = df.to_dict(orient="records")

            print(f"✅ '{student_file}' opened successfully!")

        except FileNotFoundError:
            print(f"❌ File '{student_file}' was not found.")
            continue

        except pd.errors.EmptyDataError:
            print(f"❌ '{student_file}' is empty.")
            continue

        except Exception as e:
            print(f"❌ Could not open '{student_file}'.")
            print(f"Reason: {e}")
            continue

    elif choice == "3":
        print("\n========== ADD STUDENT ==========\n")

        name = input("📑 Enter Name: ").strip()

        if name == "":
            print("❌ Name cannot be empty.")
            continue

        rollno = input("🪪 Enter Roll Number: ").strip()

        
        duplicate = False

        for student in students:
            if student["rollno"] == rollno:
                duplicate = True
                break

        if duplicate:
            print("❌ Roll Number already exists!")
            continue

        subject = input("📚 Enter Subject: ").strip()

        if subject == "":
            print("❌ Subject cannot be empty.")
            continue

        try:
            marks = int(input("🔢 Enter Marks (0-100): "))
        except ValueError:
            print("❌ Marks must be a number.")
            continue

        if marks < 0 or marks > 100:
            print("❌ Marks must be between 0 and 100.")
            continue

        grade = calculate_grade(marks)

        student = Student(rollno, name, subject, marks, grade)
        manager.add_student(student)

        df = pd.DataFrame([student.to_dict() for student in manager.get_students()])
        df.to_csv(student_file, index=False)

        print("\n✅ Student Added Successfully!")

    elif choice == "4":
        if len(manager.get_students()) == 0:
            print("❌ No students available.")
        else:
            print("\n----- Student List -----")
            print(f"📊 Total Students: {len(manager.get_students())}")
            print("=" * 40)

            for student in manager.get_students():
                print("Name :", student.name)
                print("Roll No :", student.rollno)
                print("Subject :", student.subject)
                print("Marks :", student.marks)
                print("Grade :", student.grade)
                print("=" * 40)
    elif choice == "5":
        search_rollno = input("Enter roll number to search: ")

        student = manager.search_by_rollno(search_rollno)

        if student:
            print("\n✅ Student Found")
            print("=" * 40)
            print("Name :", student.name)
            print("Roll No :", student.rollno)
            print("Subject :", student.subject)
            print("Marks :", student.marks)
            print("Grade :", student.grade)
            print("=" * 40)
        else:
            print("❌ Student not found.")
    elif choice == "6":
        update_roll = input("🪪 Enter Roll Number to update: ")

        student = manager.search_by_rollno(update_roll)

        if student:

            print("\nCurrent Details")
            print("----------------------")
            print("Name :", student.name)
            print("Subject :", student.subject)
            print("Marks :", student.marks)
            print("Grade :", student.grade)

            print("\nEnter New Details")

            student.name = input("New Name: ").strip()
            student.subject = input("New Subject: ").strip()

            try:
                student.marks = int(input("New Marks: "))
            except ValueError:
                print("❌ Invalid Marks")
                continue

            if student.marks < 0 or student.marks > 100:
                print("❌ Marks must be between 0 and 100")
                continue

            student.grade = calculate_grade(student.marks)

            df = pd.DataFrame([
                student_record.to_dict()
                for student_record in manager.get_students()
            ])

            df.to_csv(student_file, index=False)

            print("\n✅ Student Updated Successfully!")

        else:
            print("❌ Student not found.")

    elif choice == "7":
        delete_roll = input("Enter roll number to delete: ")

        student = manager.search_by_rollno(delete_roll)

        if student:
            manager.delete_student(delete_roll)

            df = pd.DataFrame([
                student_record.to_dict()
                for student_record in manager.get_students()
            ])

            df.to_csv(student_file, index=False)

            print("✅ Student deleted successfully.")
        else:
            print("❌ Student not found.")

    elif choice == "8":

        if len(students) == 0:
            print("❌ No students available.")
        else:
            marks = [student["marks"] for student in students]
            marks = np.array(marks)

            print("\n===== Student Statistics =====")
            print("Average Marks :", np.mean(marks))
            print("Highest Marks :", np.max(marks))
            print("Lowest Marks :", np.min(marks))
            print("Total Students :", len(students))

    elif choice == "9":

        subject_name = input("📚 Enter Subject: ").strip()

        subject_marks = []

        for student in students:
            if str(student["subject"]).lower() == subject_name.lower():
                subject_marks.append(student["marks"])

        if len(subject_marks) == 0:
            print("❌ No students found for this subject.")
        else:
            subject_marks = np.array(subject_marks)

            print("\n===== SUBJECT STATISTICS =====")
            print("Subject :", subject_name)
            print("Students :", len(subject_marks))
            print("Average :", np.mean(subject_marks))
            print("Highest :", np.max(subject_marks))
            print("Lowest :", np.min(subject_marks))
    elif choice == "10":

        if len(students) == 0:
            print("❌ No students available.")
            continue

        print("\n===== GRAPH MENU =====")
        print("1. Bar Chart (Students vs Marks)")
        print("2. Pie Chart (Grade Distribution)")
        print("3. Histogram (Marks)")
        print("4. Back")

        graph_choice = input("Enter your choice: ")

        if graph_choice == "1":
            names = [student["name"] for student in students]
            marks = [student["marks"] for student in students]
            plt.figure(figsize=(10, 6))
            plt.bar(names, marks, color="skyblue")
            plt.xlabel("Students")
            plt.ylabel("Marks")
            plt.title("Students vs Marks")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.show()
        elif graph_choice == "2":
            grade_counts = pd.Series([student["grade"] for student in students]).value_counts()
            plt.figure(figsize=(8, 8))
            plt.pie(grade_counts, labels=grade_counts.index, autopct="%1.1f%%", startangle=140)
            plt.title("Grade Distribution")
            plt.axis("equal")
            plt.show()
        elif graph_choice == "3":
            marks = [student["marks"] for student in students]
            plt.figure(figsize=(8, 6))
            plt.hist(marks, bins=10, color="green", edgecolor="black")
            plt.xlabel("Marks")
            plt.ylabel("Number of Students")
            plt.title("Marks Distribution")
            plt.tight_layout()
            plt.show()
        elif graph_choice == "4":
            continue
        else:
            print("❌ Invalid graph choice. Please try again.")
    elif choice == "11":

        export_to_excel(students, student_file)
    elif choice == "12":

        if len(students) == 0:
            print("❌ No student data available.")
            continue
        filename = student_file.replace(".csv", "_report.pdf")
        pdf = SimpleDocTemplate(filename)

        elements = []
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        title_style.alignment = TA_CENTER
        title_style.textColor = colors.HexColor("#1F3A5F")
        subtitle_style = styles["Heading2"]
        subtitle_style.alignment = TA_CENTER
        subtitle_style.textColor = colors.HexColor("#6B7280")

        elements.append(
            Paragraph("<b>STUDENT MANAGEMENT SYSTEM</b>", title_style)
        )

        elements.append(
            Paragraph("Student Performance Report", subtitle_style)
        )

        

        marks_list = [float(student["marks"]) for student in students]

        total_students = len(students)
        average_marks = sum(marks_list) / total_students
        highest_marks = max(marks_list)
        lowest_marks = min(marks_list)

        passed = sum(1 for marks in marks_list if marks >= 50)
        failed = total_students - passed

        summary_title = styles["Heading2"]
        summary_title.alignment = TA_CENTER
        summary_title.textColor = colors.HexColor("#1F3A5F")

        elements.append(
            Paragraph("REPORT SUMMARY", summary_title)
        )

        elements.append(Spacer(1, 10))

        summary_data = [
            ["Total Students", "Average Marks", "Highest Marks"],
            [str(total_students),
             f"{average_marks:.2f}",
             f"{highest_marks:.0f}"],

            ["Lowest Marks", "Passed", "Failed"],
            [f"{lowest_marks:.0f}",
             str(passed),
             str(failed)]
        ]

        summary_table = Table(
            summary_data,
            colWidths=[150, 150, 150]
        )

        summary_table.setStyle(TableStyle([

            ('BACKGROUND', (0, 0), (-1, 0), '#EAF0F6'),
            ('BACKGROUND', (0, 2), (-1, 2), '#EAF0F6'),

            ('TEXTCOLOR', (0, 0), (-1, -1), '#1F2937'),

            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),

            ('GRID', (0, 0), (-1, -1), 0.5, '#E5E7EB'),

        ]))

        elements.append(summary_table)

        elements.append(Spacer(1, 20))
       
        top_student = max(students, key=lambda student: float(student["marks"]))

        top_title = styles["Heading2"]
        top_title.alignment = TA_CENTER
        top_title.textColor = colors.HexColor("#1F3A5F")

        elements.append(
            Paragraph("TOP PERFORMER", top_title)
        )

        elements.append(Spacer(1, 8))

        top_data = [
            ["Name", "Subject", "Marks", "Grade"],
            [
                top_student["name"],
                top_student["subject"],
                str(top_student["marks"]),
                top_student["grade"]
            ]
        ]

        top_table = Table(
            top_data,
            colWidths=[150, 150, 75, 75]
        )

        top_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#EAF0F6'),
            ('TEXTCOLOR', (0, 0), (-1, 0), '#1F3A5F'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),

            ('GRID', (0, 0), (-1, -1), 0.5, '#D1D5DB'),
        ]))

        elements.append(top_table)

        elements.append(Spacer(1, 20))

        data = [["Roll No", "Name", "Subject", "Marks", "Grade"]]

        for student in students:
            data.append([
                student["rollno"],
                student["name"],
                student["subject"],
                student["marks"],
                student["grade"]
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#1F3A5F'),
            ('TEXTCOLOR', (0, 0), (-1, 0), '#FFFFFF'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

            ('TEXTCOLOR', (0, 1), (-1, -1), '#1F2937'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), ['#FFFFFF', '#F8FAFC']),
            ('GRID', (0, 0), (-1, -1), 0.3, '#E5E7EB'),
        ]))

        elements.append(table)
        elements.append(Paragraph("<br/><br/>", styles["Normal"]))
        now = datetime.now().strftime("%d %B %Y | %I:%M %p")

        date_style = styles["Normal"]
        date_style.alignment = TA_CENTER
        date_style.fontSize = 9
        date_style.textColor = colors.HexColor("#6B7280")

        elements.append(
            Paragraph(f"Generated on: {now}", date_style)
        )

        elements.append(Spacer(1, 18))

        pdf.build(elements)
        print(f"✅ PDF exported successfully! to {filename}")

    elif choice == "13":

        print("Thanks for using Student Management System.")
        break

    else:   
        print("❌ Invalid choice. Please try again.")