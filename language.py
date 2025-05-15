import tkinter as tk
import requests
from tkinter import messagebox

# Function to fetch trivia questions from Open Trivia API
def fetch_trivia(language_code):
    url = f'https://opentdb.com/api.php?amount=10&language={language_code}'
    response = requests.get(url)
    data = response.json()
    
    if data['response_code'] == 0:  # If API responds with trivia questions
        questions = data['results']
        return questions
    else:
        return None

# Function to start a new quiz with trivia questions
def start_quiz():
    language_code = language_var.get()
    
    if language_code:
        questions = fetch_trivia(language_code)
        
        if questions:
            show_question(questions, 0)
        else:
            messagebox.showerror("Error", "Failed to fetch trivia questions.")
    else:
        messagebox.showwarning("Input Error", "Please select a language.")

# Function to show a question and choices
def show_question(questions, question_index):
    if question_index < len(questions):
        question_data = questions[question_index]
        question_text = question_data['question']
        choices = question_data['incorrect_answers'] + [question_data['correct_answer']]
        
        # Randomly shuffle choices
        import random
        random.shuffle(choices)
        
        # Clear previous question details
        for widget in answer_frame.winfo_children():
            widget.destroy()
        
        # Display the question
        question_label.config(text=question_text)
        
        # Display answer choices as buttons
        for choice in choices:
            answer_button = tk.Button(answer_frame, text=choice, command=lambda c=choice: check_answer(c, question_data['correct_answer'], questions, question_index))
            answer_button.pack(pady=5)
    else:
        messagebox.showinfo("Quiz Complete", "You've completed the quiz!")

# Function to check if the selected answer is correct
def check_answer(selected_answer, correct_answer, questions, question_index):
    if selected_answer == correct_answer:
        messagebox.showinfo("Correct", "Well done! Your answer is correct.")
    else:
        messagebox.showinfo("Incorrect", f"Oops! The correct answer was: {correct_answer}")
    
    # Move to the next question
    show_question(questions, question_index + 1)

# Setup the main window
root = tk.Tk()
root.title("Language Learning App")

# Language selection
language_label = tk.Label(root, text="Select Language for Trivia:")
language_label.pack(pady=10)

# Language options (can be expanded)
language_var = tk.StringVar()
language_dropdown = tk.OptionMenu(root, language_var, "en", "fr", "de", "es", "it")
language_dropdown.pack(pady=10)

# Start quiz button
start_button = tk.Button(root, text="Start Quiz", command=start_quiz)
start_button.pack(pady=20)

# Question display area
question_label = tk.Label(root, text="", font=("Helvetica", 14), wraplength=400)
question_label.pack(pady=20)

# Answer choices display area
answer_frame = tk.Frame(root)
answer_frame.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()