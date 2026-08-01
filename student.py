import pandas as pd
import numpy as np
import os

FILE_NAME = "student.csv"

# Load data
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    students = df.to_dict("records")
else:
    students = []


def save_data():
    df = pd.DataFrame(students)
    df.to_csv(FILE_NAME, index=False)


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


while True:

    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Student Statistics")
    print("7. Topper")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        name = input("Enter Name: ")
        roll = input("Enter Roll Number: ")

        duplicate = False
        for s in students:
            if s["rollno"] == roll:
                duplicate = True
                break

        if duplicate:
            print("Roll number already exists!")
            continue

        marks = int(input("Enter Marks: "))

        student = {
            "name": name,
            "rollno": roll,
            "marks": marks,
            "grade": calculate_grade(marks)
        }

        students.append(student)
        save_data()
        print("Student Added Successfully.")

    elif choice == "2":

        if len(students) == 0:
            print("No students available.")

        else:
            print("\n-----------------------------------------")
            print("Name\tRoll\tMarks\tGrade")
            print("-----------------------------------------")

            for s in students:
                print(f"{s['name']}\t{s['rollno']}\t{s['marks']}\t{s['grade']}")

    elif choice == "3":

        roll = input("Enter Roll Number: ")

        found = False

        for s in students:
            if s["rollno"] == roll:
                print("\nStudent Found")
                print(s)
                found = True
                break

        if not found:
            print("Student Not Found.")

    elif choice == "4":

        roll = input("Enter Roll Number to Update: ")

        found = False

        for s in students:
            if s["rollno"] == roll:
                s["name"] = input("Enter New Name: ")
                s["marks"] = int(input("Enter New Marks: "))
                s["grade"] = calculate_grade(s["marks"])
                save_data()
                print("Student Updated Successfully.")
                found = True
                break

        if not found:
            print("Student Not Found.")

    elif choice == "5":

        roll = input("Enter Roll Number to Delete: ")

        found = False

        for s in students:
            if s["rollno"] == roll:
                students.remove(s)
                save_data()
                print("Student Deleted Successfully.")
                found = True
                break

        if not found:
            print("Student Not Found.")

    elif choice == "6":

        if len(students) == 0:
            print("No students available.")

        else:
            marks = np.array([s["marks"] for s in students])

            print("\nStudent Statistics")
            print("------------------------")
            print("Average :", np.mean(marks))
            print("Highest :", np.max(marks))
            print("Lowest  :", np.min(marks))
            print("Total Students :", len(students))

    elif choice == "7":

        if len(students) == 0:
            print("No students available.")

        else:
            topper = max(students, key=lambda x: x["marks"])

            print("\nTopper")
            print("----------------")
            print("Name :", topper["name"])
            print("Roll :", topper["rollno"])
            print("Marks:", topper["marks"])
            print("Grade:", topper["grade"])

    elif choice == "8":

        print("Thank you!")
        break

    else:
        print("Invalid Choice.")