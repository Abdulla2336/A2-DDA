import tkinter as tk
from tkinter import messagebox, ttk

# Load student data from file
def load_data():
    try:
        with open("A1 - Skills Portfolio/A1 - Resources/studentMarks.txt", "r") as file:
            lines = file.readlines()
            num_students = int(lines[0].strip())  # First line is number of students
            students = []

            for line in lines[1:num_students + 1]:
                parts = line.strip().split(",")
                student_id, name = parts[0], parts[1]
                coursework = sum(map(int, parts[2:5]))  # Sum of 3 coursework marks
                exam = int(parts[5])  # Exam mark
                total = coursework + exam
                percentage = (total / 160) * 100
                grade = calculate_grade(percentage)
                students.append((student_id, name, coursework, exam, percentage, grade))
            return students
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")
        return []

# Calculate letter grade
def calculate_grade(percentage):
    if percentage >= 70: return "A"
    elif percentage >= 60: return "B"
    elif percentage >= 50: return "C"
    elif percentage >= 40: return "D"
    else: return "F"

# Display all student records
def view_all_students():
    clear_frame()
    ttk.Label(root, text="All Student Records", font=("Arial", 16, "bold"), background="#dff0d8").pack(pady=10)
    
    for student in students:
        student_text = f"ID: {student[0]}, Name: {student[1]}, Total: {student[2] + student[3]}, Exam: {student[3]}, Percentage: {student[4]:.2f}%, Grade: {student[5]}"
        ttk.Label(root, text=student_text, background="#dff0d8").pack()

# View individual student record
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

# Show student with highest score
def show_highest():
    top_student = max(students, key=lambda s: s[2] + s[3])
    messagebox.showinfo("Top Student", f"ID: {top_student[0]}\nName: {top_student[1]}\nTotal: {top_student[2] + top_student[3]}\nPercentage: {top_student[4]:.2f}%\nGrade: {top_student[5]}")

# Show student with lowest score
def show_lowest():
    bottom_student = min(students, key=lambda s: s[2] + s[3])
    messagebox.showinfo("Lowest Student", f"ID: {bottom_student[0]}\nName: {bottom_student[1]}\nTotal: {bottom_student[2] + bottom_student[3]}\nPercentage: {bottom_student[4]:.2f}%\nGrade: {bottom_student[5]}")

# Clear the UI frame
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Main UI setup
root = tk.Tk()
root.title("Student Marks Management")
root.geometry("500x400")
root.configure(bg="#e3f2fd")

students = load_data()

# Menu
ttk.Label(root, text="Student Records System", font=("Arial", 16, "bold"), background="#e3f2fd").pack(pady=10)
ttk.Button(root, text="View All Records", command=view_all_students).pack(pady=5)
ttk.Button(root, text="View Individual Record", command=view_individual_student).pack(pady=5)
ttk.Button(root, text="Top Student", command=show_highest).pack(pady=5)
ttk.Button(root, text="Lowest Student", command=show_lowest).pack(pady=5)
ttk.Button(root, text="Exit", command=root.quit).pack(pady=5)

root.mainloop()
