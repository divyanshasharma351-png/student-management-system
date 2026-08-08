import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from datetime import datetime
student_file = ""
students = []

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

        df = pd.DataFrame(students)
        df.to_csv(student_file, index=False)

        print(f"✅ '{student_file}' created successfully!")
    elif choice == "2":
        csv_files = []

        for file in os.listdir():
            if file.endswith(".csv"):
                csv_files.append(file)

        if len(csv_files) == 0:
            print("❌ No student lists found.")
            continue

        print("\n📂 Available Student Lists:")

        for i, file in enumerate(csv_files, start=1):
            print(f"{i}. {file}")

        try:
            select = int(input("\nEnter list number: "))

            if select < 1 or select > len(csv_files):
                print("❌ Invalid choice.")
                continue

        except ValueError:
            print("❌ Please enter a number.")
            continue

        student_file = csv_files[select - 1]

        df = pd.read_csv(student_file)

        students = df.to_dict(orient="records")

        print(f"✅ '{student_file}' opened successfully!")
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

        student = {
            "name": name.title(),
            "rollno": rollno,
            "subject": subject.title(),
            "marks": marks,
            "grade": grade
        }

        students.append(student)

        df = pd.DataFrame(students)
        df.to_csv(student_file, index=False)

        print("\n✅ Student Added Successfully!")

    elif choice == "4":

        if len(students) == 0:
            print("❌ No students available.")
        else:
            print("\n----- Student List -----")
            print(f"📊 Total Students: {len(students)}")
            print("=" * 40)

            for student in students:
                print("Name :", student["name"])
                print("Roll No :", student["rollno"])
                print("Subject :", student["subject"])
                print("Marks :", student["marks"])
                print("Grade :", student["grade"])
                print("=" * 40)

    elif choice == "5":

        search_rollno = input("Enter roll number to search: ")

        found = False

        for student in students:
            if student["rollno"] == search_rollno:
                print("\n✅ Student Found")
                print("=" * 40)
                print("Name :", student["name"])
                print("Roll No :", student["rollno"])
                print("Subject :", student["subject"])
                print("Marks :", student["marks"])
                print("Grade :", student["grade"])
                print("=" * 40)

                found = True
                break

        if not found:
            print("❌ Student not found.")
    elif choice == "6":
        update_roll = input("🪪 Enter Roll Number to update: ")

        found = False

        for student in students:
            if student["rollno"] == update_roll:
                print("\nCurrent Details")
                print("----------------------")
                print("Name :", student["name"])
                print("Subject :", student["subject"])
                print("Marks :", student["marks"])
                print("Grade :", student["grade"])

                print("\nEnter New Details")

                student["name"] = input("New Name: ").strip()
                student["subject"] = input("New Subject: ").strip()

                try:
                    student["marks"] = int(input("New Marks: "))
                except ValueError:
                    print("❌ Invalid Marks")
                    break

                if student["marks"] < 0 or student["marks"] > 100:
                    print("❌ Marks must be between 0 and 100")
                    break

                student["grade"] = calculate_grade(student["marks"])

                df = pd.DataFrame(students)
                df.to_csv(student_file, index=False)

                print("\n✅ Student Updated Successfully!")

                found = True
                break

        if not found:
            print("❌ Student not found.")        

    elif choice == "7":

        delete_roll = input("Enter roll number to delete: ")

        found = False

        for student in students:
            if student["rollno"] == delete_roll:
                students.remove(student)

                df = pd.DataFrame(students)
                df.to_csv(student_file, index=False)

                print("✅ Student deleted successfully.")

                found = True
                break

        if not found:
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

        if len(students) == 0:
            print("❌ No students available.")
            continue

        wb = Workbook()
        ws = wb.active
        ws.title = "Students"

        headers = ["Name", "Roll Number", "Subject", "Marks", "Grade"]
        ws.append(headers)
        header_fill = PatternFill(fill_type="solid", fgColor="2C3E50")
        header_font = Font(
            bold=True,
            color="FFFFFF",
            size=12,
            name="Calibri"
        )
        header_alignment = Alignment(horizontal="center", vertical="center")

        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_alignment

        for student in students:
            ws.append([
                student["name"],
                student["rollno"],
                student["subject"],
                student["marks"],
                student["grade"]
            ])
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)

            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass

            ws.column_dimensions[column_letter].width = max_length + 4
        ws.freeze_panes = "A2"

        excel_file = student_file.replace(".csv", ".xlsx")
        wb.save(excel_file)

        print(f"✅ Excel file saved as '{excel_file}'")
        print("✅ Excel file created successfully! to student_report.xlsx")
    elif choice == "12":
       
        if not students:
            print("❌ No student data available!")
            continue

        filename = "student_report.pdf"
        pdf = SimpleDocTemplate(filename)

        elements = []
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        title_style.alignment = TA_CENTER
        title_style.textColor = colors.darkblue

        subtitle_style = styles["Heading2"]
        subtitle_style.alignment = TA_CENTER
        subtitle_style.textColor = colors.grey

        elements.append(
            Paragraph("<b>STUDENT MANAGEMENT SYSTEM</b>", title_style)
        )

        elements.append(
            Paragraph("Student Performance Report", subtitle_style)
        )

        elements.append(Paragraph("<br/>", styles["Normal"]))
        now = datetime.now().strftime("%d %B %Y | %I:%M %p")
        elements.append(
            Paragraph(f"<b>Generated on:</b> {now}", styles["Normal"])
        )
        elements.append(Paragraph("<br/>", styles["Normal"]))

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
            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))

        elements.append(table)
        elements.append(Paragraph("<br/><br/>", styles["Normal"]))

        now = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        elements.append(Paragraph(f"<b>Generated on:</b> {now}", styles["Normal"]))

        pdf.build(elements)
        print("✅ PDF exported successfully!")

    elif choice == "13":

        print("Thanks for using Student Management System.")
        break

    else:   
        print("❌ Invalid choice. Please try again.")