"""
Arquivo Sonoro 18.4.3 — Quiz MPB (versão profissional)

- GUI: Tkinter (interface limpa)
- 100 perguntas sobre MPB (base fornecida)
- Alternativas geradas automaticamente (4 opções por pergunta)
- Timer regressivo: 15 segundos por pergunta
- Feedback visual (correta/errada) e desabilita opções após resposta
- Ranking salvo em ranking.json (nome, pontos, total, data)
- Leaderboard (Top 10) acessível ao final
- Código organizado e comentado
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import json
import os
import datetime

# ---------------------------
# Configurações
# ---------------------------
TIME_PER_QUESTION = 20
RANKING_FILE = "ranking.json"
WINDOW_TITLE = "Arquivo Sonoro 18.4.3"

# Ranking tiers (porcentagem)
TIERS = [
    (0.95, "AMETISTA", "#9966cc"),
    (0.85, "RUBI", "#b00020"),
    (0.75, "DIAMANTE", "#00e1ff"),
    (0.60, "OURO", "#ffd700"),
    (0.40, "PRATA", "#c0c0c0"),
    (0.0, "BRONZE", "#cd7f32"),
]

# Pool de nomes/possíveis alternativas (usado para gerar distractors)
NAMES_POOL = [
    "Tom Jobim", "Vinícius de Moraes", "João Gilberto", "Chico Buarque",
    "Caetano Veloso", "Gilberto Gil", "Milton Nascimento", "Djavan",
    "Alceu Valença", "Belchior", "Elis Regina", "Baden Powell",
    "Toquinho", "Paulinho da Viola", "Zé Ramalho", "Raul Seixas",
    "Roberto Carlos", "Lô Borges", "Humberto Teixeira", "Cartola",
    "Aldir Blanc", "João Bosco", "Jorge Ben Jor", "Renato Teixeira",
    "Almir Sater", "Los Hermanos", "Herbert Vianna", "Los Hermanos",
    "Edu Lobo", "Newton Mendonça", "Ary Barroso", "Luiz Bonfá",
    "Pixinguinha", "Ronaldo Bôscoli", "Roberto Menescal", "Renato Russo"
]

YEARS_POOL = ["1958", "1959", "1960", "1962", "1965", "1970", "1972", "1974", "1975", "1980", "1984", "1990"]

# ---------------------------
# Banco de perguntas (100)
# (usadas as perguntas da sua lista — mantive exatamente o texto que você enviou)
# ---------------------------
RAW_QUESTIONS = [
    ("Quem compôs 'Chega de Saudade'?", "Tom Jobim e Vinícius de Moraes"),
    ("O álbum 'Chega de Saudade' de João Gilberto é de qual ano?", "1959"),
    ("Quem compôs 'Construção'?", "Chico Buarque"),
    ("Qual álbum marca o Clube da Esquina?", "Clube da Esquina (1972)"),
    ("Quem compôs 'Águas de Março'?", "Tom Jobim"),
    ("Qual álbum Elis Regina gravou com Tom Jobim?", "Elis & Tom"),
    ("Caetano Veloso liderou qual movimento?", "Tropicália"),
    ("Quem era o vocalista da Legião Urbana?", "Renato Russo"),
    ("Quem compôs 'Garota de Ipanema'?", "Tom Jobim e Vinícius de Moraes"),
    ("Quem lançou o álbum 'Transa'?", "Caetano Veloso"),
    ("Quem compôs 'Tocando em Frente'?", "Renato Teixeira e Almir Sater"),
    ("Quem idealizou 'Panis et Circencis'?", "Caetano Veloso e Gilberto Gil"),
    ("Quem compôs 'O Bêbado e a Equilibrista'?", "Aldir Blanc e João Bosco"),
    ("Quem gravou o álbum 'Elis' (1972)?", "Elis Regina"),
    ("Quem compôs 'Asa Branca'?", "Luiz Gonzaga e Humberto Teixeira"),
    ("Quem compôs 'Desafinado'?", "Tom Jobim e Newton Mendonça"),
    ("Quem é a figura central do Clube da Esquina?", "Milton Nascimento"),
    ("Quem compôs 'Manhã de Carnaval'?", "Luiz Bonfá"),
    ("Quem compôs 'Detalhes'?", "Roberto Carlos"),
    ("Quem compôs 'Carinhoso'?", "Pixinguinha"),
    ("Quem compôs 'Disparada'?", "Geraldo Vandré e Théo de Barros"),
    ("Quem compôs 'O Trem Azul'?", "Lô Borges e Milton Nascimento"),
    ("Quem compôs 'O Leãozinho'?", "Caetano Veloso"),
    ("Quem compôs 'Sina'?", "Djavan"),
    ("Quem compôs 'Tristeza'?", "Haroldo Lobo e Nássara"),
    ("Quem compôs 'Ponta de Areia'?", "Milton Nascimento"),
    ("Quem compôs 'Fio Maravilha'?", "Jorge Ben Jor"),
    ("Quem compôs 'Romaria'?", "Renato Teixeira"),
    ("Quem compôs 'Aquarela do Brasil'?", "Ary Barroso"),
    ("Quem compôs 'A Felicidade'?", "Tom Jobim e Vinícius de Moraes"),
    ("Quem compôs 'O Mundo é um Moinho'?", "Cartola"),
    ("Quem compôs 'Trem das Onze'?", "Adoniran Barbosa"),
    ("Quem compôs 'O Que Será (À Flor da Pele)'?", "Chico Buarque"),
    ("Quem compôs 'Ponteio'?", "Edu Lobo e Capinan"),
    ("'Flor de Lis' é de qual compositor?", "Djavan"),
    ("Quem compôs 'Travessia'?", "Milton Nascimento"),
    ("Quem compôs 'Oração ao Tempo'?", "Caetano Veloso"),
    ("Quem compôs 'Lanterna dos Afogados'?", "Herbert Vianna (Paralamas)"),
    ("Quem compôs 'Anna Júlia'?", "Los Hermanos"),
    ("Quem compôs 'Meu Bem Querer'?", "Djavan"),
    ("Quem compôs 'Aquarela'?", "Toquinho e Vinícius"),
    ("Quem compôs 'Que Maravilha'?", "Jorge Ben Jor"),
    ("Quem cantou a versão famosa de 'The Girl from Ipanema'?", "Astrud Gilberto"),
    ("Qual dupla compôs 'Chega de Saudade'?", "Tom Jobim e Vinícius de Moraes"),
    ("De quem é a canção 'Sampa'?", "Caetano Veloso"),
    ("De quem é a canção 'Apesar de Você'?", "Chico Buarque"),
    ("De quem é 'Asa Branca'?", "Luiz Gonzaga e Humberto Teixeira"),
    ("De quem é 'Ponta de Areia'?", "Milton Nascimento"),
    ("Quem compôs 'Oração ao Tempo'?", "Caetano Veloso"),
    ("Quem compôs 'Disparada'?", "Geraldo Vandré e Théo de Barros"),
    ("Quem compôs 'Fio Maravilha'?", "Jorge Ben Jor"),
    ("Quem compôs 'Carinhoso'?", "Pixinguinha"),
    ("Quem compôs 'Flor de Lis'?", "Djavan"),
    ("Quem compôs 'O Mundo é um Moinho'?", "Cartola"),
    ("Quem compôs 'Travessia'?", "Milton Nascimento"),
    ("Quem compôs 'O Trem Azul'?", "Lô Borges e Milton"),
    ("Quem compôs 'Detalhes'?", "Roberto Carlos"),
    ("Quem compôs 'Garota de Ipanema'?", "Tom Jobim e Vinícius de Moraes"),
    ("Quem compôs 'Cálice'?", "Chico Buarque"),
    ("Quem compôs 'Canto de Ossanha'?", "Baden Powell e Vinícius"),
    ("Quem compôs 'Berimbau'?", "Baden Powell e Vinícius"),
    ("Quem compôs 'As Curvas da Estrada de Santos'?", "Roberto e Erasmo Carlos"),
    ("Quem compôs 'Foi um Rio que Passou em Minha Vida'?", "Paulinho da Viola"),
    ("Quem compôs 'O Morro Não Tem Vez'?", "Tom Jobim e Vinícius"),
    ("Quem compôs 'Tarde em Itapoã'?", "Toquinho e Vinícius"),
    ("Quem compôs 'Samba de Uma Nota Só'?", "Tom Jobim e Newton Mendonça"),
    ("Quem compôs 'Onde Anda Você'?", "Vinícius de Moraes e Hermínio Bello de Carvalho"),
    ("Quem compôs 'Eu Sei que Vou Te Amar'?", "Tom Jobim e Vinícius"),
    ("Quem compôs 'Se Todos Fossem Iguais a Você'?", "Tom Jobim e Vinícius"),
    ("Quem compôs 'O Barquinho'?", "Roberto Menescal e Ronaldo Bôscoli"),
    ("Quem compôs 'Corcovado'?", "Tom Jobim"),
    ("Quem compôs 'Terra'?", "Caetano Veloso"),
    ("Quem compôs 'Nos Bailes da Vida'?", "Milton Nascimento"),
    ("Quem compôs 'Maria, Maria'?", "Milton Nascimento"),
    ("Quem compôs 'Canção da América'?", "Milton Nascimento"),
    ("Quem compôs 'A Lua Girou'?", "Milton Nascimento"),
    ("Quem compôs 'Reconvexo'?", "Caetano Veloso"),
    ("Quem compôs 'Oração Latina'?", "Milton Nascimento"),
    ("Quem compôs 'Wave'?", "Tom Jobim"),
    ("Quem compôs 'Samba do Avião'?", "Tom Jobim"),
    ("Quem compôs 'Garoto de Aluguel'?", "Zé Ramalho"),
    ("Quem compôs 'Admirável Gado Novo'?", "Zé Ramalho"),
    ("Quem compôs 'Chão de Giz'?", "Zé Ramalho"),
    ("Quem compôs 'Metamorfose Ambulante'?", "Raul Seixas"),
    ("Quem compôs 'Gita'?", "Raul Seixas"),
    ("Quem compôs 'Maluco Beleza'?", "Raul Seixas"),
    ("Quem compôs 'Como Nossos Pais'?", "Belchior"),
    ("Quem compôs 'Velha Roupa Colorida'?", "Belchior"),
    ("Quem compôs 'Apenas um Rapaz Latino-Americano'?", "Belchior"),
    ("Quem compôs 'Pavão Mysteriozo'?", "Ednardo"),
    ("Quem compôs 'Tropicana'?", "Alceu Valença"),
    ("Quem compôs 'Anunciação'?", "Alceu Valença"),
    ("Quem compôs 'La Belle de Jour'?", "Alceu Valença"),
]

# ---------------------------
# Funções utilitárias
# ---------------------------

def load_ranking():
    """Carrega ranking do arquivo (se existir)."""
    if not os.path.exists(RANKING_FILE):
        return []
    try:
        with open(RANKING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_ranking(entry):
    """Salva um novo registro de ranking."""
    data = load_ranking()
    data.append(entry)
    # ordena por pontos decrescentes
    data = sorted(data, key=lambda x: x.get("pontos", 0), reverse=True)
    try:
        with open(RANKING_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Erro ao salvar ranking:", e)

def format_datetime_now():
    return datetime.datetime.now().isoformat(timespec="seconds")

def determine_tier(score, total):
    pct = score / total if total else 0
    for threshold, name, color in TIERS:
        if pct >= threshold:
            return name, color
    return "BRONZE", "#cd7f32"

def generate_options(correct_answer):
    """
    Gera 4 alternativas (incluindo a correta).
    Estratégia:
    - Se resposta contém dígitos (ano) -> usa YEARS_POOL
    - Se resposta contém '&' ou 'e' ou ',' (múltiplos autores) -> tenta usar outros nomes compostos
    - Caso contrário usa NAMES_POOL
    """
    correct = correct_answer
    options = set()
    options.add(correct)

    # detectar se é ano (apenas dígitos)
    if correct.strip().isdigit():
        pool = list(set(YEARS_POOL + [str(int(correct) + d) for d in (-2, -1, 1, 2, 3)]))
        pool = [p for p in pool if p != correct]
        while len(options) < 4 and pool:
            options.add(random.choice(pool))
    else:
        # usar NAMES_POOL para distractors
        # normalizar: se resposta contiver ' e ' ou ' & ' ou ',' então trata como entry composta
        pool = NAMES_POOL.copy()
        # garantir que a resposta exata não se repita em pool
        for p in [correct] + correct.split(" e "):
            if p in pool:
                pool.remove(p)
        # compor alternativas únicas
        while len(options) < 4 and pool:
            candidate = random.choice(pool)
            options.add(candidate)
            pool.remove(candidate)

    # se não chegou a 4 (por qualquer motivo), completar com placeholders
    fillers = ["Vários artistas", "Desconhecido", "Outro autor", "Sem informação"]
    while len(options) < 4:
        options.add(random.choice(fillers))

    options_list = list(options)
    random.shuffle(options_list)
    return options_list

# ---------------------------
# Preparar perguntas com alternativas
# ---------------------------

QUESTIONS = []
for q_text, q_answer in RAW_QUESTIONS:
    opts = generate_options(q_answer)
    QUESTIONS.append({
        "question": q_text,
        "answer": q_answer,
        "options": opts
    })

random.shuffle(QUESTIONS)

# ---------------------------
# Classe do App
# ---------------------------

class QuizApp:
    def __init__(self, master, questions):
        self.master = master
        self.master.title(WINDOW_TITLE)
        self.master.geometry("900x600")
        self.questions = questions
        self.total = len(self.questions)
        self.index = 0
        self.score = 0
        self.time_left = TIME_PER_QUESTION
        self.timer_job = None
        self.answered = False

        self._build_ui()
        self._load_question()

    def _build_ui(self):
        # topo: título e placar
        top_frame = tk.Frame(self.master, bg="#111")
        top_frame.pack(fill="x", padx=12, pady=8)

        title = tk.Label(top_frame, text="Arquivo Sonoro 18.4.3 — Quiz MPB", font=("Helvetica", 22, "bold"),
                         fg="white", bg="#111")
        title.pack(side="left")

        self.score_label = tk.Label(top_frame, text=f"Pontuação: 0/{self.total}", font=("Helvetica", 14),
                                    fg="white", bg="#111")
        self.score_label.pack(side="right", padx=8)

        # pergunta
        self.question_frame = tk.Frame(self.master, bg="#222", padx=16, pady=12, relief="groove", bd=2)
        self.question_frame.pack(fill="both", expand=False, padx=12, pady=(6, 12))

        self.question_label = tk.Label(self.question_frame, text="", font=("Helvetica", 18), fg="white", bg="#222",
                                       wraplength=820, justify="left")
        self.question_label.pack(anchor="w")

        # opções (radiobuttons)
        self.options_var = tk.StringVar(value="")
        self.options_frame = tk.Frame(self.master, bg="#111")
        self.options_frame.pack(fill="both", padx=12)

        self.option_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(self.options_frame, text="", value="", variable=self.options_var, command=self._on_select)
            rb.pack(anchor="w", pady=6, padx=8, fill="x")
            self.option_buttons.append(rb)

        # timer e controles
        bottom_frame = tk.Frame(self.master, bg="#111")
        bottom_frame.pack(fill="x", padx=12, pady=12)

        self.timer_label = tk.Label(bottom_frame, text=f"Tempo: {TIME_PER_QUESTION}s", font=("Helvetica", 14, "bold"),
                                    fg="#ff4444", bg="#111")
        self.timer_label.pack(side="left")

        self.progress = ttk.Progressbar(bottom_frame, orient="horizontal", length=300, mode="determinate",
                                        maximum=TIME_PER_QUESTION)
        self.progress.pack(side="left", padx=10)

        self.feedback_label = tk.Label(bottom_frame, text="", font=("Helvetica", 12), fg="white", bg="#111")
        self.feedback_label.pack(side="left", padx=10)

        btn_frame = tk.Frame(bottom_frame, bg="#111")
        btn_frame.pack(side="right")

        self.next_button = tk.Button(btn_frame, text="Confirmar / Próxima", command=self._confirm_or_next, font=("Helvetica", 12))
        self.next_button.pack(side="left", padx=6)

        self.skip_button = tk.Button(btn_frame, text="Pular", command=self._skip_question, font=("Helvetica", 12))
        self.skip_button.pack(side="left", padx=6)

        self.leaderboard_button = tk.Button(btn_frame, text="Leaderboard", command=self._show_leaderboard, font=("Helvetica", 12))
        self.leaderboard_button.pack(side="left", padx=6)

    def _load_question(self):
        """Carrega a pergunta atual e reinicia o timer."""
        self.answered = False
        self.options_var.set("")
        self.feedback_label.config(text="", fg="white")
        self.time_left = TIME_PER_QUESTION
        self.progress['value'] = 0
        self._update_timer_label()

        q = self.questions[self.index]
        self.question_label.config(text=f"{self.index + 1}. {q['question']}")

        # colocar opções nos radiobuttons
        for rb, opt in zip(self.option_buttons, q['options']):
            rb.config(text=opt, value=opt)
            rb.state(["!disabled"])

        # iniciar timer
        if self.timer_job:
            self.master.after_cancel(self.timer_job)
        self.timer_job = self.master.after(1000, self._tick)

        # atualizar placar
        self.score_label.config(text=f"Pontuação: {self.score}/{self.total}")

    def _tick(self):
        """Atualiza timer a cada segundo; avança quando tempo esgota."""
        self.time_left -= 1
        elapsed = TIME_PER_QUESTION - self.time_left
        if elapsed < 0: elapsed = 0
        self.progress['value'] = elapsed
        self._update_timer_label()

        if self.time_left <= 0:
            # tempo esgotou: considera como pular/errado
            self.feedback_label.config(text="Tempo esgotado!", fg="#ffaaaa")
            self._reveal_answer()
            self.master.after(1500, self._go_to_next)
        else:
            self.timer_job = self.master.after(1000, self._tick)

    def _update_timer_label(self):
        self.timer_label.config(text=f"Tempo: {self.time_left}s")

    def _on_select(self):
        # limpar feedback ao selecionar
        self.feedback_label.config(text="", fg="white")

    def _confirm_or_next(self):
        """Se não respondeu ainda, avalia; se já respondeu, vai pra próxima."""
        if not self.answered:
            selected = self.options_var.get()
            if selected == "":
                messagebox.showinfo("Atenção", "Escolha uma alternativa ou pressione Pular.")
                return
            self._evaluate(selected)
        else:
            self._go_to_next()

    def _evaluate(self, selected):
        """Avalia resposta selecionada e dá feedback."""
        self.answered = True
        correct = self.questions[self.index]['answer']
        if self.timer_job:
            self.master.after_cancel(self.timer_job)

        if selected.strip().lower() == correct.strip().lower():
            self.score += 1
            self.feedback_label.config(text="Correto!", fg="#aaffaa")
        else:
            self.feedback_label.config(text=f"Errado! Resposta: {correct}", fg="#ffaaaa")

        # desabilitar opções
        for rb in self.option_buttons:
            rb.state(["disabled"])

        # atualizar placar
        self.score_label.config(text=f"Pontuação: {self.score}/{self.total}")

        # trocar texto do botão para "Próxima"
        self.next_button.config(text="Próxima")
        # avançar automaticamente após 1.2s
        self.master.after(1200, self._go_to_next)

    def _reveal_answer(self):
        """Revela a resposta correta visualmente (quando tempo esgota)."""
        self.answered = True
        correct = self.questions[self.index]['answer']
        self.feedback_label.config(text=f"Tempo! Resposta: {correct}", fg="#ffaaaa")
        for rb in self.option_buttons:
            rb.state(["disabled"])
        self.next_button.config(text="Próxima")

    def _go_to_next(self):
        """Avança para a próxima pergunta ou finaliza o quiz."""
        if self.timer_job:
            try:
                self.master.after_cancel(self.timer_job)
            except Exception:
                pass
            self.timer_job = None

        self.index += 1
        if self.index >= self.total:
            self._end_quiz()
            return
        # carregar próxima pergunta
        self.next_button.config(text="Confirmar / Próxima")
        self._load_question()

    def _skip_question(self):
        """Pula a pergunta atual (não soma pontos)."""
        if self.timer_job:
            self.master.after_cancel(self.timer_job)
            self.timer_job = None
        self.feedback_label.config(text="Pergunta pulada.", fg="#ffffaa")
        for rb in self.option_buttons:
            rb.state(["disabled"])
        self.next_button.config(text="Próxima")
        self.master.after(600, self._go_to_next)

    def _end_quiz(self):
        """Mostra resultado, pede nome e salva ranking."""
        # calcular tier
        tier_name, tier_color = determine_tier(self.score, self.total)

        # pedir nome
        nome = simpledialog.askstring("Fim do Quiz", f"Você fez {self.score}/{self.total} pontos.\nNível: {tier_name}\n\nNome para o ranking:")
        if nome:
            entry = {
                "nome": nome,
                "pontos": self.score,
                "total": self.total,
                "percentual": round((self.score / self.total) * 100, 2),
                "nivel": tier_name,
                "data": format_datetime_now()
            }
            save_ranking(entry)

        # resumo final
        messagebox.showinfo("Fim", f"Resultado: {self.score}/{self.total}\nNível: {tier_name}")

        # oferecer leaderboard
        if messagebox.askyesno("Leaderboard", "Deseja ver o leaderboard (Top 10)?"):
            self._show_leaderboard()
        self.master.destroy()

    def _show_leaderboard(self):
        data = load_ranking()
        if not data:
            messagebox.showinfo("Leaderboard", "Nenhum registro encontrado.")
            return
        # top 10
        top = data[:10]

        # criar janela para leaderboard
        win = tk.Toplevel(self.master)
        win.title("Leaderboard — Top 10")
        win.geometry("600x400")
        frm = tk.Frame(win, padx=12, pady=12)
        frm.pack(fill="both", expand=True)

        header = tk.Label(frm, text=f"Leaderboard — Top 10", font=("Helvetica", 16, "bold"))
        header.pack(pady=(0,8))

        tree = ttk.Treeview(frm, columns=("nome","pontos","percentual","nivel","data"), show="headings", height=10)
        tree.heading("nome", text="Nome")
        tree.heading("pontos", text="Pontos")
        tree.heading("percentual", text="%")
        tree.heading("nivel", text="Nível")
        tree.heading("data", text="Data")
        tree.column("nome", width=180)
        tree.column("pontos", width=80, anchor="center")
        tree.column("percentual", width=80, anchor="center")
        tree.column("nivel", width=100, anchor="center")
        tree.column("data", width=140, anchor="center")

        for row in top:
            tree.insert("", tk.END, values=(row.get("nome"), f"{row.get('pontos')}/{row.get('total')}", row.get("percentual"), row.get("nivel"), row.get("data")))

        tree.pack(fill="both", expand=True)

        btn_close = tk.Button(frm, text="Fechar", command=win.destroy)
        btn_close.pack(pady=8)

# ---------------------------
# Inicializar app
# ---------------------------
def main():
    root = tk.Tk()
    root.configure(bg="#111")
    app = QuizApp(root, QUESTIONS)
    root.mainloop()

if __name__ == "__main__":
    main()
