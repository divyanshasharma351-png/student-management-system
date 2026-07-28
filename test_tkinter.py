import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Student Management System")
app.geometry("700x500")

label = ctk.CTkLabel(
    app,
    text="Student Management System",
    font=("Arial", 24, "bold")
)
label.pack(pady=30)

app.mainloop()