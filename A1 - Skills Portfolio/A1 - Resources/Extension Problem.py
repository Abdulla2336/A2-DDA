import tkinter as tk
from tkinter import messagebox, ttk
import os

FILE_NAME = "studentMarks.txt"

# Load student data from file
def load_data():
    if not os.path.exists(FILE_NAME):
        return []
    with open("A1 - Skills Portfolio/A1 - Resources/studentMarks.txt", "r") as file:
        lines = file.readlines()
        if not lines:
            return []
        num_students = int(lines[0].strip())
        students = []
        for line in lines[1:num_students + 1]:
            parts = line.strip().split(",")
            student_id, name = parts[0], parts[1]
            coursework = sum(map(int, parts[2:5]))
            exam = int(parts[5])
            total = coursework + exam
            percentage = (total / 160) * 100
            grade = calculate_grade(percentage)
            students.append((student_id, name, coursework, exam, percentage, grade))
        return students

# Save data back to file
def save_data():
    with open("A1 - Skills Portfolio/A1 - Resources/studentMarks.txt", "w") as file:
        file.write(f"{len(students)}\n")
        for s in students:
            file.write(f"{s[0]},{s[1]},{s[2]//3},{s[2]//3},{s[2]//3},{s[3]}\n")

# Grade Calculation
def calculate_grade(percentage):
    return "A" if percentage >= 70 else "B" if percentage >= 60 else "C" if percentage >= 50 else "D" if percentage >= 40 else "F"

# UI Frame Reset
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# View All Records
def view_all_students():
    clear_frame()
    ttk.Label(root, text="All Student Records", font=("Arial", 16, "bold"), background="#dff0d8").pack(pady=10)
    for student in students:
        text = f"ID: {student[0]}, Name: {student[1]}, Total: {student[2] + student[3]}, Exam: {student[3]}, Percentage: {student[4]:.2f}%, Grade: {student[5]}"
        ttk.Label(root, text=text, background="#dff0d8").pack()

# View Individual Student Record
def view_individual_student():
    def search_student():
        student_id = entry.get()
        student = next((s for s in students if s[0] == student_id), None)
        if student:
            messagebox.showinfo("Student Record", f"ID: {student[0]}\nName: {student[1]}\nTotal: {student[2] + student[3]}\nExam: {student[3]}\nPercentage: {student[4]:.2f}%\nGrade: {student[5]}")
        else:
            messagebox.showerror("Error", "Student not found")
    
    clear_frame()
    ttk.Label(root, text="Enter Student ID:", font=("Arial", 12), background="#fcf8e3").pack(pady=5)
    entry = ttk.Entry(root)
    entry.pack(pady=5)
    ttk.Button(root, text="Search", command=search_student).pack(pady=5)

# Show Student with Highest and Lowest Scores
def show_highest():
    if not students:
        messagebox.showwarning("No Data", "No student records available.")
        return
    student = max(students, key=lambda s: s[2] + s[3])
    messagebox.showinfo("Top Student", f"ID: {student[0]}\nName: {student[1]}\nTotal: {student[2] + student[3]}\nPercentage: {student[4]:.2f}%\nGrade: {student[5]}")

def show_lowest():
    if not students:
        messagebox.showwarning("No Data", "No student records available.")
        return
    student = min(students, key=lambda s: s[2] + s[3])
    messagebox.showinfo("Lowest Student", f"ID: {student[0]}\nName: {student[1]}\nTotal: {student[2] + student[3]}\nPercentage: {student[4]:.2f}%\nGrade: {student[5]}")


# Sort Student Records
def sort_students(ascending=True):
    students.sort(key=lambda s: s[2] + s[3], reverse=not ascending)
    view_all_students()

# Add Student
def add_student():
    def save_student():
        student_id, name, c1, c2, c3, exam = entry_id.get(), entry_name.get(), entry_c1.get(), entry_c2.get(), entry_c3.get(), entry_exam.get()
        if not all([student_id, name, c1, c2, c3, exam]):
            messagebox.showerror("Error", "All fields are required")
            return
        coursework = sum(map(int, [c1, c2, c3]))
        total = coursework + int(exam)
        percentage = (total / 160) * 100
        grade = calculate_grade(percentage)
        students.append((student_id, name, coursework, int(exam), percentage, grade))
        save_data()
        messagebox.showinfo("Success", "Student added successfully!")
        menu()

    clear_frame()
    ttk.Label(root, text="Add New Student", font=("Arial", 16, "bold"), background="#cfe2ff").pack(pady=10)
    ttk.Label(root, text="ID:").pack()
    entry_id = ttk.Entry(root)
    entry_id.pack()
    ttk.Label(root, text="Name:").pack()
    entry_name = ttk.Entry(root)
    entry_name.pack()
    ttk.Label(root, text="Coursework Marks (3 values):").pack()
    entry_c1, entry_c2, entry_c3 = ttk.Entry(root), ttk.Entry(root), ttk.Entry(root)
    entry_c1.pack(), entry_c2.pack(), entry_c3.pack()
    ttk.Label(root, text="Exam Mark:").pack()
    entry_exam = ttk.Entry(root)
    entry_exam.pack()
    ttk.Button(root, text="Save", command=save_student).pack(pady=5)

# Delete Student
def delete_student():
    def confirm_delete():
        student_id = entry.get()
        global students
        students = [s for s in students if s[0] != student_id]
        save_data()
        messagebox.showinfo("Deleted", "Student record deleted")
        menu()
    
    clear_frame()
    ttk.Label(root, text="Enter Student ID to Delete:", font=("Arial", 12), background="#f8d7da").pack(pady=5)
    entry = ttk.Entry(root)
    entry.pack()
    ttk.Button(root, text="Delete", command=confirm_delete).pack(pady=5)

# Main Menu
def menu():
    clear_frame()
    ttk.Label(root, text="Student Management System", font=("Arial", 16, "bold"), background="#e3f2fd").pack(pady=10)
    buttons = [("View All", view_all_students), ("View One", view_individual_student), ("Highest", show_highest), ("Lowest", show_lowest),
               ("Sort ↑", lambda: sort_students(True)), ("Sort ↓", lambda: sort_students(False)), ("Add", add_student), ("Delete", delete_student), ("Exit", root.quit)]
    for text, cmd in buttons:
        ttk.Button(root, text=text, command=cmd).pack(pady=5)

# Initialize
root = tk.Tk()
root.title("Student Management")
root.geometry("500x500")
root.configure(bg="#e3f2fd")

students = load_data()
menu()

root.mainloop()
