import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

student_file = "student.csv"


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


if os.path.exists(student_file):
    df = pd.read_csv(student_file)
    students = df.to_dict(orient="records")
else:
    students = []

while True:

    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    
    choice = input("Enter your choice: ")

    if choice == "1":
        print("\n========== ADD STUDENT ==========\n")

        name = input("📑 Enter Name: ").strip()

        if name == "":
            print("❌ Name cannot be empty.")
            continue

        rollno = input("🪪 Enter Roll Number: ").strip()

        # Check duplicate roll number
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

    elif choice == "2":

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

    elif choice == "3":

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
    elif choice == "4":
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

    elif choice == "5":

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

    elif choice == "6":

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

    elif choice == "7":

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
    elif choice == "8":

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
    elif choice == "9":

        print("Thanks for using Student Management System.")
        break

    else:   
        print("❌ Invalid choice. Please try again.")