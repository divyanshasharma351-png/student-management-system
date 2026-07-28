import csv
import customtkinter as ctk
import sys,subprocess
from tkinter import messagebox


def save_student(name, roll, marks):
    with open("student.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, roll, marks])

    messagebox.showinfo("Success", "Student saved successfully!")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Student Management System")
app.geometry("1000x650")


sidebar = ctk.CTkFrame(app, width=220, corner_radius=0)
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(
    sidebar,
    text="🎓\nStudent\nManagement",
    font=("Arial", 22, "bold")
)
logo.pack(pady=30)


main = ctk.CTkFrame(app)
main.pack(side="right", fill="both", expand=True, padx=15, pady=15)


def clear_main():
    for widget in main.winfo_children():
        widget.destroy()



def show_add_student():
    clear_main()

    title = ctk.CTkLabel(
        main,
        text="➕ Add Student",
        font=("Arial", 28, "bold")
    )
    title.pack(pady=20)

    name_entry = ctk.CTkEntry(
        main,
        width=350,
        placeholder_text="Enter Student Name"
    )
    name_entry.pack(pady=10)

    roll_entry = ctk.CTkEntry(
        main,
        width=350,
        placeholder_text="Enter Roll Number"
    )
    roll_entry.pack(pady=10)

    marks_entry = ctk.CTkEntry(
        main,
        width=350,
        placeholder_text="Enter Marks"
    )
    marks_entry.pack(pady=10)

    button_frame = ctk.CTkFrame(main, fg_color="transparent")
    button_frame.pack(pady=20)

    save_btn = ctk.CTkButton(
        button_frame,
        text="💾 Save",
        width=150,
        command=lambda: save_student(
            name_entry.get(),
            roll_entry.get(),
            marks_entry.get()
        )
    )
    save_btn.grid(row=0, column=0, padx=10)

    clear_btn = ctk.CTkButton(
        button_frame,
        text="🧹 Clear",
        width=150,
        command=show_add_student
    )
    clear_btn.grid(row=0, column=1, padx=10)



dashboard_btn = ctk.CTkButton(
    sidebar,
    text="🏠 Dashboard",
    width=180
)
dashboard_btn.pack(pady=8)

add_btn = ctk.CTkButton(
    sidebar,
    text="➕ Add Student",
    width=180,
    command=show_add_student
)
add_btn.pack(pady=8)

view_btn = ctk.CTkButton(
    sidebar,
    text="👀 View Students",
    width=180
)
view_btn.pack(pady=8)

search_btn = ctk.CTkButton(
    sidebar,
    text="🔍 Search Student",
    width=180
)
search_btn.pack(pady=8)

update_btn = ctk.CTkButton(
    sidebar,
    text="✏️ Update Student",
    width=180
)
update_btn.pack(pady=8)

delete_btn = ctk.CTkButton(
    sidebar,
    text="🗑 Delete Student",
    width=180
)
delete_btn.pack(pady=8)

stats_btn = ctk.CTkButton(
    sidebar,
    text="📊 Statistics",
    width=180
)
stats_btn.pack(pady=8)

exit_btn = ctk.CTkButton(
    sidebar,
    text="🚪 Exit",
    width=180,
    command=app.destroy
)
exit_btn.pack(side="bottom", pady=20)

show_add_student()

app.mainloop()