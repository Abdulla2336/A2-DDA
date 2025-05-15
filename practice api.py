import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import html
import time

# === Modern Styling ===
BG_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"
TEXT_COLOR = "#E2E8F0"
SCORE_COLOR = "#38BDF8"
WRONG_COLOR = "#EF4444"
CORRECT_COLOR = "#22C55E"
BUTTON_COLOR = "#3B82F6"
TIMER_COLOR = "#FBBF24"
ACCENT_ORANGE = "#FB923C"

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_QUESTION = ("Segoe UI", 15)
FONT_BUTTON = ("Segoe UI", 13, "bold")

# === OpenTDB API ===
API_URL = "https://opentdb.com/api.php"
API_PARAMETERS = {
    "amount": 10,
    "category": 15,
    "type": "boolean",
}

# === Fallback Questions ===
FALLBACK_QUESTIONS = [
    {"question": "Is Pac-Man a game character?", "correct_answer": True},
    {"question": "The game 'Fortnite' was released before 2015.", "correct_answer": False},
    {"question": "'The Legend of Zelda' was first released in the 1980s.", "correct_answer": True},
    {"question": "You can tame a dragon in 'Minecraft'.", "correct_answer": False},
    {"question": "Sonic the Hedgehog is a Nintendo character.", "correct_answer": False},
]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Pixel Brain: The Ultimate Game Quiz")
        self.root.config(bg=BG_COLOR, padx=40, pady=30)
        self.root.resizable(False, False)

        self.questions = []
        self.score = 0
        self.current_question_index = 0
        self.timer = None
        self.time_left = 10

        self.create_widgets()

    def create_widgets(self):
        self.greeting_label = tk.Label(
            self.root,
            text="🎯 Welcome to Pixel Brain!\nPress 'Start Quiz' to begin.",
            font=FONT_TITLE,
            fg=SCORE_COLOR,
            bg=BG_COLOR,
            justify="center"
        )
        self.greeting_label.grid(column=0, row=0, columnspan=3, pady=15)

        self.score_label = tk.Label(self.root, text="Score: 0", font=FONT_TITLE, fg=SCORE_COLOR, bg=BG_COLOR)
        self.score_label.grid(column=2, row=1, sticky="e")

        self.timer_label = tk.Label(self.root, text="", font=FONT_BUTTON, fg=TIMER_COLOR, bg=BG_COLOR)
        self.timer_label.grid(column=1, row=1)

        self.question_card = tk.Canvas(self.root, bg=CARD_COLOR, width=600, height=250, highlightthickness=0)
        self.question_card.grid(column=0, row=2, columnspan=3, pady=25)
        self.question_text = self.question_card.create_text(
            300, 125, text="", font=FONT_QUESTION, fill=TEXT_COLOR, width=500
        )

        self.start_button = tk.Button(
            self.root,
            text="Start Quiz",
            font=FONT_BUTTON,
            fg="white",
            bg=BUTTON_COLOR,
            activebackground="#60A5FA",
            width=15,
            command=self.start_quiz,
        )
        self.start_button.grid(column=1, row=3, pady=15)

        self.true_button = tk.Button(
            self.root,
            text="True",
            font=FONT_BUTTON,
            fg="white",
            bg=CORRECT_COLOR,
            activebackground="#4ADE80",
            width=10,
            command=lambda: self.check_answer(True),
        )
        self.true_button.grid(column=0, row=3)
        self.true_button.grid_forget()

        self.false_button = tk.Button(
            self.root,
            text="False",
            font=FONT_BUTTON,
            fg="white",
            bg=WRONG_COLOR,
            activebackground="#F87171",
            width=10,
            command=lambda: self.check_answer(False),
        )
        self.false_button.grid(column=2, row=3)
        self.false_button.grid_forget()

        self.restart_button = tk.Button(
            self.root,
            text="Restart Quiz",
            font=FONT_BUTTON,
            fg="white",
            bg=ACCENT_ORANGE,
            activebackground="#FDBA74",
            width=15,
            command=self.restart_quiz,
        )
        self.restart_button.grid(column=1, row=4, pady=10)
        self.restart_button.grid_forget()

    def fetch_questions(self):
        last_exception = None
        for attempt in range(3):
            try:
                response = requests.get(API_URL, params=API_PARAMETERS, timeout=20)
                response.raise_for_status()
                data = response.json()

                if data.get("response_code") == 0 and "results" in data:
                    return [
                        {
                            "question": html.unescape(q["question"]),
                            "correct_answer": q["correct_answer"].lower() == "true",
                        }
                        for q in data["results"]
                    ]
                else:
                    raise ValueError("Invalid response format or empty result.")
            except (requests.RequestException, ValueError) as e:
                last_exception = e
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2)

        messagebox.showwarning(
            "Network Error",
            "Unable to connect to OpenTDB API after several attempts.\nUsing fallback questions.\n\nError details:\n"
            f"{last_exception}"
        )
        return FALLBACK_QUESTIONS

    def start_quiz(self):
        self.questions = self.fetch_questions()
        if not self.questions:
            self.question_card.itemconfig(self.question_text, text="No questions available.")
            return

        self.score = 0
        self.current_question_index = 0
        self.greeting_label.grid_forget()
        self.start_button.grid_forget()
        self.true_button.grid(column=0, row=3)
        self.false_button.grid(column=2, row=3)
        self.update_question()

    def update_question(self):
        if self.current_question_index >= len(self.questions):
            self.end_quiz()
        else:
            question = self.questions[self.current_question_index]
            self.question_card.itemconfig(self.question_text, text=question["question"])
            self.question_card.config(bg=CARD_COLOR)
            self.time_left = 10
            self.start_timer()

    def start_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.time_left -= 1
            self.timer = self.root.after(1000, self.start_timer)
        else:
            self.timer_label.config(text="Time's up!")
            self.current_question_index += 1
            self.root.after(800, self.update_question)

    def check_answer(self, user_answer):
        if self.timer:
            self.root.after_cancel(self.timer)
        correct_answer = self.questions[self.current_question_index]["correct_answer"]
        if user_answer == correct_answer:
            self.score += 1
            self.question_card.config(bg=CORRECT_COLOR)
        else:
            self.question_card.config(bg=WRONG_COLOR)

        self.score_label.config(text=f"Score: {self.score}")
        self.current_question_index += 1
        self.root.after(800, self.update_question)

    def end_quiz(self):
        self.true_button.grid_forget()
        self.false_button.grid_forget()
        self.restart_button.grid(column=1, row=4)
        self.question_card.itemconfig(
            self.question_text, text=f"🎉 Quiz Over!\nFinal Score: {self.score} / {len(self.questions)}"
        )
        self.timer_label.config(text="")

    def restart_quiz(self):
        if self.timer:
            self.root.after_cancel(self.timer)
        self.restart_button.grid_forget()
        self.greeting_label.grid(column=0, row=0, columnspan=3, pady=15)
        self.start_button.grid(column=1, row=3, pady=15)
        self.question_card.itemconfig(self.question_text, text="")
        self.score_label.config(text="Score: 0")
        self.timer_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
