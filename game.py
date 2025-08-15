import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

class FunWordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Wizard")
        self.root.geometry("500x500")
        self.root.configure(bg="#FFD700")  # Gold background
        
        # Game words by category
        self.categories = {
            "Fruits": ['apple', 'banana', 'orange', 'mango', 'kiwi', 'peach'],
            "Animals": ['dog', 'cat', 'lion', 'frog', 'bear', 'fish'],
            "Colors": ['red', 'blue', 'green', 'pink', 'black', 'white']
        }
        
        # Game variables
        self.current_category = "Fruits"
        self.secret_word = ""
        self.display_word = []
        self.attempts = 6
        self.guessed_letters = []
        
        # Load happy/sad emoji images
        try:
            self.happy_img = ImageTk.PhotoImage(Image.open("happy.png").resize((100, 100)))
            self.sad_img = ImageTk.PhotoImage(Image.open("sad.png").resize((100, 100)))
        except:
            self.happy_img = None
            self.sad_img = None
        
        # Create GUI
        self.create_widgets()
        self.new_game()
    
    def create_widgets(self):
        """Create all the game widgets"""
        # Header
        header_frame = tk.Frame(self.root, bg="#FF6347")  # Tomato color
        header_frame.pack(fill="x", pady=10)
        
        self.title_label = tk.Label(
            header_frame,
            text="WORD WIZARD",
            font=("Comic Sans MS", 24, "bold"),
            bg="#FF6347",
            fg="white"
        )
        self.title_label.pack(pady=5)
        
        # Category buttons
        cat_frame = tk.Frame(self.root, bg="#FFD700")
        cat_frame.pack(pady=5)
        
        for category in self.categories:
            btn = tk.Button(
                cat_frame,
                text=category,
                command=lambda c=category: self.set_category(c),
                font=("Arial", 10, "bold"),
                bg="#9370DB",  # Medium purple
                fg="white",
                activebackground="#8A2BE2"  # Blue violet
            )
            btn.pack(side="left", padx=5)
        
        # Word display
        self.word_frame = tk.Frame(self.root, bg="#FFD700")
        self.word_frame.pack(pady=20)
        
        self.word_label = tk.Label(
            self.word_frame,
            text="",
            font=("Arial", 28, "bold"),
            bg="#FFD700",
            fg="#4169E1"  # Royal blue
        )
        self.word_label.pack()
        
        # Emoji feedback
        self.emoji_label = tk.Label(self.root, bg="#FFD700")
        self.emoji_label.pack()
        
        # Attempts display
        self.attempts_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12, "bold"),
            bg="#FFD700",
            fg="#FF4500"  # Orange red
        )
        self.attempts_label.pack(pady=5)
        
        # Guessed letters
        self.guessed_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            bg="#FFD700",
            fg="#2E8B57"  # Sea green
        )
        self.guessed_label.pack()
        
        # Input area
        input_frame = tk.Frame(self.root, bg="#FFD700")
        input_frame.pack(pady=15)
        
        tk.Label(
            input_frame,
            text="Your guess:",
            font=("Arial", 12),
            bg="#FFD700"
        ).pack()
        
        self.guess_entry = tk.Entry(
            input_frame,
            font=("Arial", 18),
            width=3,
            justify="center"
        )
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind("<Return>", lambda e: self.check_guess())
        
        # Action buttons
        btn_frame = tk.Frame(self.root, bg="#FFD700")
        btn_frame.pack(pady=10)
        
        self.guess_btn = tk.Button(
            btn_frame,
            text="Guess!",
            command=self.check_guess,
            font=("Arial", 12, "bold"),
            bg="#32CD32",  # Lime green
            fg="white",
            activebackground="#228B22"  # Forest green
        )
        self.guess_btn.pack(side="left", padx=10)
        
        self.new_btn = tk.Button(
            btn_frame,
            text="New Game",
            command=self.new_game,
            font=("Arial", 12, "bold"),
            bg="#1E90FF",  # Dodger blue
            fg="white",
            activebackground="#0000CD"  # Medium blue
        )
        self.new_btn.pack(side="left", padx=10)
    
    def set_category(self, category):
        """Set the current word category"""
        self.current_category = category
        self.new_game()
    
    def new_game(self):
        """Start a new game"""
        self.secret_word = random.choice(self.categories[self.current_category])
        self.display_word = ["_"] * len(self.secret_word)
        self.attempts = 6
        self.guessed_letters = []
        
        self.update_display()
        self.guess_entry.delete(0, tk.END)
        self.guess_btn.config(state="normal")
        self.guess_entry.focus()
        
        # Reset emoji
        if self.happy_img:
            self.emoji_label.config(image=self.happy_img)
    
    def update_display(self):
        """Update the game display"""
        self.word_label.config(text=" ".join(self.display_word))
        self.attempts_label.config(text=f"❤️ Attempts left: {self.attempts}")
        self.guessed_label.config(text=f"Guessed: {', '.join(sorted(self.guessed_letters))}")
        
        # Update emoji based on attempts
        if self.attempts <= 2 and self.sad_img:
            self.emoji_label.config(image=self.sad_img)
        elif self.happy_img:
            self.emoji_label.config(image=self.happy_img)
    
    def check_guess(self):
        """Check the player's guess"""
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)
        
        # Validate input
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Oops!", "Please enter a single letter")
            return
        
        if guess in self.guessed_letters:
            messagebox.showinfo("Already guessed", f"You already tried '{guess}'")
            return
        
        self.guessed_letters.append(guess)
        
        # Check if letter is in word
        if guess in self.secret_word:
            for i in range(len(self.secret_word)):
                if self.secret_word[i] == guess:
                    self.display_word[i] = guess
            messagebox.showinfo("Great!", f"Correct! '{guess}' is in the word")
        else:
            self.attempts -= 1
            messagebox.showerror("Wrong", f"Sorry, '{guess}' isn't in the word")
        
        self.update_display()
        
        # Check win/lose conditions
        if "_" not in self.display_word:
            messagebox.showinfo(
                "You won!",
                f"Awesome! The word was {self.secret_word.upper()}\n\n"
                f"You had {self.attempts} attempts remaining!"
            )
            self.guess_btn.config(state="disabled")
        elif self.attempts == 0:
            messagebox.showinfo(
                "Game Over",
                f"Better luck next time!\n\nThe word was {self.secret_word.upper()}"
            )
            self.guess_btn.config(state="disabled")

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = FunWordGame(root)
    root.mainloop()