import tkinter as tk
import random

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.root.configure(bg="#e3f2fd")
        
        self.score = 0
        self.attempts = 0
        self.question_count = 0
        self.difficulty = None
        
        self.display_menu()
    
    def display_menu(self):
        self.clear_window()
        
        tk.Label(self.root, text="Select Difficulty Level", font=("Arial", 16, "bold"), bg="#e3f2fd").pack(pady=10)
        
        tk.Button(self.root, text="Easy", font=("Arial", 12), bg="#81C784", fg="white", command=lambda: self.start_quiz(1)).pack(pady=5)
        tk.Button(self.root, text="Moderate", font=("Arial", 12), bg="#FFD54F", fg="black", command=lambda: self.start_quiz(2)).pack(pady=5)
        tk.Button(self.root, text="Advanced", font=("Arial", 12), bg="#E57373", fg="white", command=lambda: self.start_quiz(3)).pack(pady=5)
    
    def start_quiz(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.question_count = 0
        self.next_question()
    
    def random_int(self):
        ranges = {1: (1, 9), 2: (10, 99), 3: (1000, 9999)}
        return random.randint(*ranges[self.difficulty])
    
    def decide_operation(self):
        return random.choice(['+', '-'])
    
    def next_question(self):
        if self.question_count == 10:
            self.display_results()
            return
        
        self.num1 = self.random_int()
        self.num2 = self.random_int()
        self.operation = self.decide_operation()
        
        if self.operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1
        
        self.correct_answer = eval(f"{self.num1} {self.operation} {self.num2}")
        self.attempts = 0
        self.display_problem()
    
    def display_problem(self):
        self.clear_window()
        
        tk.Label(self.root, text=f"{self.num1} {self.operation} {self.num2} =", font=("Arial", 16, "bold"), bg="#e3f2fd").pack(pady=10)
        self.answer_entry = tk.Entry(self.root, font=("Arial", 14), justify='center')
        self.answer_entry.pack(pady=5)
        self.answer_entry.bind("<Return>", lambda event: self.check_answer())
        
        tk.Button(self.root, text="Submit", font=("Arial", 12), bg="#64B5F6", fg="white", command=self.check_answer).pack(pady=5)
    
    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            tk.Label(self.root, text="Please enter a valid number", fg="red", bg="#e3f2fd").pack()
            return
        
        if user_answer == self.correct_answer:
            points = 10 if self.attempts == 0 else 5
            self.score += points
            self.question_count += 1
            self.next_question()
        else:
            self.attempts += 1
            if self.attempts == 1:
                tk.Label(self.root, text="Incorrect! Try again.", fg="red", bg="#e3f2fd").pack()
            else:
                self.question_count += 1
                self.next_question()
    
    def display_results(self):
        self.clear_window()
        
        grade = "F"
        if self.score >= 90:
            grade = "A+"
        elif self.score >= 80:
            grade = "A"
        elif self.score >= 70:
            grade = "B"
        elif self.score >= 60:
            grade = "C"
        elif self.score >= 50:
            grade = "D"
        
        tk.Label(self.root, text=f"Final Score: {self.score}/100", font=("Arial", 16, "bold"), bg="#e3f2fd").pack(pady=10)
        tk.Label(self.root, text=f"Grade: {grade}", font=("Arial", 16, "bold"), bg="#e3f2fd").pack(pady=5)
        
        tk.Button(self.root, text="Play Again", font=("Arial", 12), bg="#81C784", fg="white", command=self.display_menu).pack(pady=5)
        tk.Button(self.root, text="Exit", font=("Arial", 12), bg="#E57373", fg="white", command=self.root.quit).pack(pady=5)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    app = ArithmeticQuiz(root)
    root.mainloop()
