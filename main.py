import pandas as pd
import numpy as np
students = []

while True:

    print("\n=== STUDENT MANAGEMENT SYSTEM ===")
    print("1️⃣ Add Student")
    print("2️⃣ View Student")
    print("3️⃣ Search Student")
    print("4️⃣ Delete Student")
    print("5️⃣ Student Statistics")
    print("6️⃣ Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        name = input("📑 Enter the name: ")
        rollno = input("🪪 Enter the roll number: ")

        try:
            marks = int(input("🔢 Enter the marks: "))
        except ValueError:
            print("❌ Please enter valid marks.")
            continue

        if marks >= 90:
            grade = "A+"
        elif marks >= 80:
            grade = "A"
        elif marks >= 70:
            grade = "B"
        elif marks >= 60:
            grade = "C"
        elif marks >= 50:
            grade = "D"
        else:
            grade = "Fail"

        student = {
            "name": name,
            "rollno": rollno,
            "marks": marks,
            "grade": grade
        }

        students.append(student)

        df = pd.DataFrame(students)
        df.to_csv("student.csv", index=False)

        print("\n✅ Student added successfully.")

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
                print("Marks :", student["marks"])
                print("Grade :", student["grade"])
                print("=" * 40)

                found = True
                break

        if not found:
            print("❌ Student not found.")

    elif choice == "4":

        delete_roll = input("Enter roll number to delete: ")

        found = False

        for student in students:

            if student["rollno"] == delete_roll:

                students.remove(student)

                df = pd.DataFrame(students)
                df.to_csv("student.csv", index=False)

                print("✅ Student deleted successfully.")

                found = True
                break

        if not found:
            print("❌ Student not found.")

    elif choice == "5":

        if len(students) == 0:
            print("❌ No students available.")

        else:

            marks = []

            for student in students:
                marks.append(student["marks"])

            marks = np.array(marks)

            print("\n===== Student Statistics =====")
            print("Average Marks :", np.mean(marks))
            print("Highest Marks :", np.max(marks))
            print("Lowest Marks :", np.min(marks))
            print("Total Students :", len(students))

    elif choice == "6":

        print("Thanks for using Student Management System.")
        break

    else:
        print("❌ Invalid choice. Please try again.")