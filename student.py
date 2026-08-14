class Student:
    """Represents a single student record."""

    def __init__(self, rollno, name, subject, marks, grade):
        self.rollno = rollno
        self.name = name
        self.subject = subject
        self.marks = marks
        self.grade = grade

    def to_dict(self):
        """Convert student information into a dictionary."""
        return {
            "rollno": self.rollno,
            "name": self.name,
            "subject": self.subject,
            "marks": self.marks,
            "grade": self.grade
        }


class StudentManager:
    """Manages a collection of student records."""

    def __init__(self):
        self.students = []

    def add_student(self, student):
        """Add a student to the list."""
        self.students.append(student)

    def get_students(self):
        """Return all students."""
        return self.students

    def search_by_rollno(self, rollno):
        """Find a student using their roll number."""
        for student in self.students:
            if student.rollno == rollno:
                return student

        return None

    def delete_student(self, rollno):
        """Delete a student using their roll number."""
        for student in self.students:
            if student.rollno == rollno:
                self.students.remove(student)
                return True

        return False