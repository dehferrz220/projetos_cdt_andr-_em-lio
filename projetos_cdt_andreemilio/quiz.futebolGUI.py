import tkinter as tk
from tkinter import messagebox
import random
import os

# =========================================
# CONFIGURAÇÕES
# =========================================

APP_TITLE = "Arquivo Esportivo 18.4.3"
TIME_PER_QUESTION = 15
RANKING_FILE = "ranking.txt"

THEMES = {
    "Copa do Mundo": "#1E8449",
    "UCL": "#922B21",
    "Eurocopa": "#566573",
    "Brasileirão": "#1F618D",
    "Libertadores": "#B7950B"
}

# =========================================
# QUESTÕES (EXEMPLO — BASE SIMPLES)
# =========================================

QUESTIONS = {
    "Copa do Mundo": [
        ("Quem venceu a Copa de 1970?", ["Brasil", "Itália", "Alemanha", "Uruguai"], "Brasil"),
        ("Onde foi a Copa de 2014?", ["Brasil", "Alemanha", "Rússia", "Qatar"], "Brasil"),
        ("Quem venceu a Copa de 2022?", ["Argentina", "França", "Brasil", "Croácia"], "Argentina"),
    ],

    "UCL": [
        ("Qual clube tem mais Champions?", ["Real Madrid", "Milan", "Liverpool", "Barcelona"], "Real Madrid"),
        ("Quem venceu a Champions 2023?", ["Manchester City", "Inter", "Real Madrid", "Bayern"], "Manchester City"),
    ],

    "Eurocopa": [
        ("Quem venceu a Euro 2016?", ["Portugal", "França", "Alemanha", "Espanha"], "Portugal"),
        ("Quem venceu a Euro 2021?", ["Itália", "Inglaterra", "França", "Portugal"], "Itália"),
    ],

    "Brasileirão": [
        ("Quem venceu o Brasileirão de 2019?", ["Flamengo", "Palmeiras", "Santos", "Grêmio"], "Flamengo"),
        ("Quem venceu o Brasileirão de 2023?", ["Palmeiras", "Botafogo", "Flamengo", "Grêmio"], "Palmeiras"),
    ],

    "Libertadores": [
        ("Quem venceu a Libertadores 2019?", ["Flamengo", "River Plate", "Palmeiras", "Grêmio"], "Flamengo"),
        ("Quem venceu a Libertadores 2023?", ["Fluminense", "Boca Juniors", "Palmeiras", "Grêmio"], "Fluminense"),
    ]
}

# =========================================
# QUIZ
# =========================================

class Quiz:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("800x500")
        self.root.configure(bg="black")

        self.player = ""
        self.score = 0
        self.combo = 0
        self.index = 0
        self.time_left = TIME_PER_QUESTION
        self.paused = False

        self.start_screen()

    # -------------------------------------

    def start_screen(self):
        self.clear()

        tk.Label(
            self.root,
            text=APP_TITLE,
            font=("Helvetica", 24, "bold"),
            bg="black",
            fg="white"
        ).pack(pady=30)

        self.name_entry = tk.Entry(self.root, font=("Helvetica", 14), justify="center")
        self.name_entry.pack(pady=10)
        self.name_entry.insert(0, "Nome do jogador")

        for mode in QUESTIONS.keys():
            tk.Button(
                self.root,
                text=mode,
                font=("Helvetica", 13),
                width=25,
                bg=THEMES[mode],
                fg="white",
                command=lambda m=mode: self.start_quiz(m)
            ).pack(pady=6)

        tk.Button(
            self.root,
            text="TOP 10",
            font=("Helvetica", 12),
            command=self.show_ranking
        ).pack(pady=20)

    # -------------------------------------

    def start_quiz(self, mode):
        self.player = self.name_entry.get().strip() or "Jogador"
        self.mode = mode
        self.questions = QUESTIONS[mode][:]
        random.shuffle(self.questions)

        self.score = 0
        self.combo = 0
        self.index = 0
        self.next_question()

    # -------------------------------------

    def next_question(self):
        if self.index >= len(self.questions):
            self.finish()
            return

        self.clear()
        self.time_left = TIME_PER_QUESTION
        self.paused = False

        question, options, self.correct = self.questions[self.index]

        tk.Label(
            self.root,
            text=f"Tempo: {self.time_left}s",
            font=("Helvetica", 12),
            bg="black",
            fg="white"
        ).pack(pady=5)

        self.timer_label = self.root.winfo_children()[-1]

        tk.Label(
            self.root,
            text=question,
            font=("Helvetica", 16),
            wraplength=700,
            bg="black",
            fg="white"
        ).pack(pady=30)

        for opt in options:
            tk.Button(
                self.root,
                text=opt,
                font=("Helvetica", 12),
                width=30,
                command=lambda o=opt: self.answer(o)
            ).pack(pady=4)

        tk.Button(
            self.root,
            text="⏸ Pausar",
            command=self.toggle_pause
        ).pack(pady=10)

        self.countdown()

    # -------------------------------------

    def countdown(self):
        if not self.paused and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Tempo: {self.time_left}s")
            self.root.after(1000, self.countdown)
        elif self.time_left == 0:
            self.combo = 0
            random.shuffle(self.questions)
            self.index += 1
            self.next_question()

    # -------------------------------------

    def toggle_pause(self):
        self.paused = not self.paused
        if not self.paused:
            self.countdown()

    # -------------------------------------

    def answer(self, answer):
        if answer == self.correct:
            self.combo += 1
            self.score += 2 if self.combo >= 2 else 1
        else:
            self.combo = 0
            random.shuffle(self.questions)

        self.index += 1
        self.next_question()

    # -------------------------------------

    def finish(self):
        rank = (
            "GERACIONAL" if self.score <= 4 else
            "ICÔNICO" if self.score <= 8 else
            "LEGENDÁRIO"
        )

        with open(RANKING_FILE, "a", encoding="utf-8") as f:
            f.write(f"{self.player} - {self.score} pts - {rank}\n")

        messagebox.showinfo(
            "Fim de Jogo",
            f"Jogador: {self.player}\nPontuação: {self.score}\nRanking: {rank}"
        )

        self.start_screen()

    # -------------------------------------

    def show_ranking(self):
        if not os.path.exists(RANKING_FILE):
            messagebox.showinfo("TOP 10", "Nenhum ranking salvo.")
            return

        with open(RANKING_FILE, encoding="utf-8") as f:
            lines = f.readlines()[:10]

        messagebox.showinfo("TOP 10", "".join(lines))

    # -------------------------------------

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# =========================================
# EXECUÇÃO
# =========================================

if __name__ == "__main__":
    root = tk.Tk()
    Quiz(root)
    root.mainloop()
