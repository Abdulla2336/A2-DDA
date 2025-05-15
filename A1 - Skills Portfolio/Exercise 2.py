import tkinter as tk
import random

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa, Tell Me a Joke")
        self.root.configure(bg="#FFEBB5")
        
        self.load_jokes()
        
        self.setup_label = tk.Label(root, text="Click below for a joke!", font=("Arial", 14, "bold"), bg="#FFEBB5")
        self.setup_label.pack(pady=10)
        
        self.joke_button = tk.Button(root, text="Tell me a joke", font=("Arial", 12), bg="#FF5733", fg="white", command=self.show_joke)
        self.joke_button.pack(pady=5)
        
        self.punchline_button = tk.Button(root, text="See Punchline", font=("Arial", 12), bg="#33B5E5", fg="white", command=self.show_punchline)
        self.punchline_button.pack(pady=5)
        self.punchline_button.config(state=tk.DISABLED)
        
        self.punchline_label = tk.Label(root, text="", font=("Arial", 12, "italic"), bg="#FFEBB5")
        self.punchline_label.pack(pady=10)
        
        tk.Button(root, text="Exit", font=("Arial", 12), bg="#C70039", fg="white", command=root.quit).pack(pady=5)
    
    def load_jokes(self):
        with open("A1 - Skills Portfolio/A1 - Resources/randomJokes.txt", "r") as file:
            self.jokes = [line.strip().split("?") for line in file.readlines()]
    
    def show_joke(self):
        self.current_joke = random.choice(self.jokes)
        self.setup_label.config(text=self.current_joke[0] + "?")
        self.punchline_label.config(text="")
        self.punchline_button.config(state=tk.NORMAL)
    
    def show_punchline(self):
        self.punchline_label.config(text=self.current_joke[1])
        self.punchline_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x250")
    app = JokeApp(root)
    root.mainloop()
