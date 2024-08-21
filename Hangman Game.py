import random
import tkinter as tk
from tkinter import messagebox

# Définition des thèmes et mots
THEMES = {
    "Animaux": [("elephant", "Un grand mammifère terrestre avec une trompe."),
                ("lion", "Le roi de la jungle."),
                ("papillon", "Un insecte coloré avec des ailes.")],
    "Technologie": [("ordinateur", "Un appareil pour exécuter des programmes."),
                    ("internet", "Le réseau mondial de communication."),
                    ("robot", "Une machine programmable qui peut exécuter des tâches.")],
    "Sport": [("football", "Un jeu où on essaie de marquer des buts avec un ballon."),
              ("basketball", "Un sport où on fait rebondir une balle et tire dans un panier."),
              ("tennis", "Un jeu où les joueurs frappent une balle au-dessus d'un filet.")]
}

HANGMAN_STAGES = [
    """
       -----
       |   |
           |
           |
           |
           |
    ---------
    """,
    """
       -----
       |   |
       O   |
           |
           |
           |
    ---------
    """,
    """
       -----
       |   |
       O   |
       |   |
           |
           |
    ---------
    """,
    """
       -----
       |   |
       O   |
      /|   |
           |
           |
    ---------
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
           |
           |
    ---------
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
      /    |
           |
    ---------
    """,
    """
       -----
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    ---------
    """
]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu du Pendu")
        self.root.configure(bg='#d0f4de')
        self.word = ""
        self.hint = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.wrong_letters = []
        self.score = 0
        self.diamonds = 0
        self.total_score = 0  # Score total pour toutes les victoires

        self.theme = tk.StringVar(value="Animaux")
        theme_label = tk.Label(root, text="Choisissez un thème:", font=("Helvetica", 14), bg='#d0f4de')
        theme_label.pack(pady=5)
        theme_frame = tk.Frame(root, bg='#d0f4de')
        theme_frame.pack(pady=5)
        for theme in THEMES.keys():
            tk.Radiobutton(theme_frame, text=theme, variable=self.theme, value=theme, font=("Helvetica", 12), bg='#d0f4de').pack(side=tk.LEFT)

        self.start_button = tk.Button(root, text="Commencer", font=("Helvetica", 14), command=self.start_game, bg='#ff6f61')
        self.start_button.pack(pady=10)

        self.hangman_label = tk.Label(root, text=self.get_hangman_stage(), font=("Courier", 18), justify="left", bg='#d0f4de')
        self.word_label = tk.Label(root, text="", font=("Helvetica", 18), bg='#d0f4de')
        self.hint_label = tk.Label(root, text="", font=("Helvetica", 14), bg='#d0f4de')
        self.wrong_letters_label = tk.Label(root, text="Lettres incorrectes : ", font=("Helvetica", 14), bg='#d0f4de')
        self.score_label = tk.Label(root, text=f"Score: {self.total_score} | Diamants: {self.diamonds}", font=("Helvetica", 14), bg='#d0f4de')
        self.input_entry = tk.Entry(root, font=("Helvetica", 14))
        self.guess_button = tk.Button(root, text="Devinez", font=("Helvetica", 14), command=self.guess_letter, bg='#ff6f61')
        self.reset_button = tk.Button(root, text="Rejouer", font=("Helvetica", 14), command=self.reset_game, state=tk.DISABLED, bg='#ff6f61')
        self.quit_button = tk.Button(root, text="Abandonner", font=("Helvetica", 14), command=root.quit, bg='#ff6f61')
        self.rules_button = tk.Button(root, text="Règles", font=("Helvetica", 14), command=self.show_rules, bg='#ff6f61')

        self.setup_ui()

    def setup_ui(self):
        self.hangman_label.pack(pady=10)
        self.word_label.pack(pady=10)
        self.hint_label.pack(pady=5)
        self.wrong_letters_label.pack(pady=10)
        self.score_label.pack(pady=5)
        self.input_entry.pack(pady=10)
        self.guess_button.pack(pady=10)
        self.reset_button.pack(pady=10)
        self.quit_button.pack(pady=10)
        self.rules_button.pack(pady=10)

    def get_hangman_stage(self):
        return HANGMAN_STAGES[self.wrong_guesses] if 0 <= self.wrong_guesses < len(HANGMAN_STAGES) else HANGMAN_STAGES[-1]

    def start_game(self):
        selected_theme = self.theme.get()
        self.word, self.hint = random.choice(THEMES[selected_theme])
        self.word = self.word.upper()
        self.guessed_letters.clear()
        self.wrong_guesses = 0
        self.wrong_letters.clear()
        self.update_display()

        self.reset_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)
        self.guess_button.config(state=tk.NORMAL)

    def update_display(self):
        self.hangman_label.config(text=self.get_hangman_stage())
        self.word_label.config(text=self.display_word())
        self.hint_label.config(text=f"Indice : {self.hint}")
        self.wrong_letters_label.config(text=f"Lettres incorrectes : {' '.join(self.wrong_letters)}")
        self.score_label.config(text=f"Score Total: {self.total_score} | Diamants: {self.diamonds}")

    def display_word(self):
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])

    def guess_letter(self, event=None):
        guess = self.input_entry.get().upper()
        self.input_entry.delete(0, tk.END)
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Entrée invalide", "Veuillez entrer une seule lettre.")
            return
        if guess in self.guessed_letters or guess in self.wrong_letters:
            messagebox.showwarning("Lettre déjà devinée", f"Vous avez déjà deviné la lettre '{guess}'.")
        elif guess in self.word:
            self.guessed_letters.add(guess)
        else:
            self.wrong_letters.append(guess)
            self.wrong_guesses += 1
        self.update_display()
        self.check_game_over()

    def check_game_over(self):
        if set(self.word) == self.guessed_letters:
            # Calcul du score pour cette victoire
            score_for_this_win = len(self.word) * (7 - self.wrong_guesses)
            self.total_score += score_for_this_win
            self.diamonds += 1
            self.display_victory_animation()
            messagebox.showinfo("Victoire", f"Félicitations! Vous avez deviné le mot '{self.word}'.")
            self.end_game()
        elif self.wrong_guesses == len(HANGMAN_STAGES) - 1:
            self.display_defeat_animation()
            messagebox.showinfo("Défaite", f"Vous avez perdu! Le mot était '{self.word}'.")
            self.end_game()

    def display_victory_animation(self):
        colors = ['#ffeb3b', '#f44336', '#2196f3', '#4caf50']
        token_size = 50  # Taille des "jetons"

        # Création d'un cadre pour afficher les "jetons"
        token_frame = tk.Frame(self.root, bg='#d0f4de')
        token_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def animate_tokens():
            for _ in range(30):  # Nombre de "jetons"
                x = random.randint(50, 300)
                y = random.randint(50, 300)
                color = random.choice(colors)

                # Création d'un jeton circulaire pour simuler un pion de Ludo
                token = tk.Canvas(token_frame, width=token_size, height=token_size, bg=color, highlightthickness=0)
                token.create_oval(5, 5, token_size - 5, token_size - 5, fill=color)
                token.place(x=x, y=y, anchor=tk.CENTER)

                # Déplacer et supprimer le jeton après un court délai
                def move_token(token):
                    for _ in range(10):  # Nombre de déplacements
                        self.root.after(_, lambda: token.place(x=random.randint(50, 300), y=random.randint(50, 300)))
                    self.root.after(1000, token.place_forget)

                self.root.after(100, move_token, token)

        animate_tokens()
        self.display_fireworks()
        self.display_smiles()

    def display_fireworks(self):
        # Animation des feux d'artifice
        fireworks_colors = ['#ff0000', '#ff9900', '#33cc33', '#00ccff', '#ff00ff', '#00ff00', '#0000ff']
        for _ in range(30):  # Nombre de feux d'artifice
            color = random.choice(fireworks_colors)
            firework = tk.Canvas(self.root, width=100, height=100, bg='black', highlightthickness=0)
            firework.place(relx=random.random(), rely=random.random(), anchor=tk.CENTER)

            for _ in range(30):  # Nombre de lignes par feu d'artifice
                x = random.randint(0, 100)
                y = random.randint(0, 100)
                firework.create_line(50, 50, x, y, fill=color, width=2)
                self.root.update()
                self.root.after(10)

            firework.place_forget()

    def display_smiles(self):
        # Animation des sourires
        smile_size = 50
        smile_colors = ['#ffcc00', '#ff9966', '#66ff66']
        smile_frame = tk.Frame(self.root, bg='#d0f4de')
        smile_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def create_smile():
            for _ in range(20):  # Nombre de sourires
                x = random.randint(50, 300)
                y = random.randint(50, 300)
                color = random.choice(smile_colors)

                smile = tk.Canvas(smile_frame, width=smile_size, height=smile_size, bg=color, highlightthickness=0)
                smile.create_oval(5, 5, smile_size - 5, smile_size - 5, fill=color)
                smile.place(x=x, y=y, anchor=tk.CENTER)

                self.root.after(200, smile.place_forget)  # Temps d'affichage réduit

        create_smile()

    def display_defeat_animation(self):
        # Animation pour la défaite
        colors = ['#ff0000', '#ff4d4d']
        token_size = 30

        # Création d'un cadre pour afficher les "jetons"
        token_frame = tk.Frame(self.root, bg='#d0f4de')
        token_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        def animate_tokens():
            for _ in range(20):  # Nombre de "jetons"
                x = random.randint(50, 300)
                y = random.randint(50, 300)
                color = random.choice(colors)

                # Création d'un jeton circulaire pour simuler un pion de Ludo
                token = tk.Canvas(token_frame, width=token_size, height=token_size, bg=color, highlightthickness=0)
                token.create_oval(5, 5, token_size - 5, token_size - 5, fill=color)
                token.place(x=x, y=y, anchor=tk.CENTER)

                # Déplacer et supprimer le jeton après un court délai
                def move_token(token):
                    for _ in range(10):  # Nombre de déplacements
                        self.root.after(_, lambda: token.place(x=random.randint(50, 300), y=random.randint(50, 300)))
                    self.root.after(1000, token.place_forget)

                self.root.after(100, move_token, token)

        animate_tokens()

    def end_game(self):
        self.reset_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        self.guess_button.config(state=tk.DISABLED)

    def reset_game(self):
        self.start_button.config(state=tk.NORMAL)
        self.guess_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.word = ""
        self.hint = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.wrong_letters = []
        self.update_display()

    def show_rules(self):
        rules_text = (
            "Règles du Jeu du Pendu :\n\n"
            "1. Vous devez deviner un mot caché une lettre à la fois.\n"
            "2. Chaque lettre correcte sera révélée dans le mot.\n"
            "3. Chaque lettre incorrecte ajoutera une partie au dessin du pendu.\n"
            "4. Le jeu se termine lorsque vous devinez toutes les lettres ou que le dessin du pendu est complet.\n"
            "5. Vous pouvez gagner des points et des diamants pour chaque victoire.\n"
            "6. Essayez de deviner le mot avant que le pendu soit complet!"
        )
        messagebox.showinfo("Règles du Jeu", rules_text)

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
