from tkinter import *
import random

quiz = Tk()

h = quiz.winfo_screenheight()
w = quiz.winfo_screenwidth()

question_bank = [
    {"question": "Which fundamental interaction is responsible for beta decay in radioactive atoms?",
     "choices": ["strong force", "electromagnetic force", "weak nuclear force", "gravitational force"],
     "answer": "weak nuclear force"},

    {"question": "What structure in eukaryotic cells is primarily responsible for modifying, sorting, and packaging proteins?",
     "choices": ["lysosome", "golgi apparatus", "endoplasmic reticulum", "nucleolus"],
     "answer": "golgi apparatus"},

    {"question": "Which principle states that the position and momentum of a particle cannot both be precisely determined at the same time?",
     "choices": ["pauli exclusion principle", "uncertainty principle", "superposition principle", "complementarity principle"],
     "answer": "uncertainty principle"},

    {"question": "Which geological process is primarily responsible for the creation of mountain ranges like the Himalayas?",
     "choices": ["volcanism", "plate subduction", "seafloor spreading", "continental collision"],
     "answer": "continental collision"},

    {"question": "Which law quantifies the force between two point charges?",
     "choices": ["newton’s third law", "coulomb’s law", "ohm’s law", "faraday’s law"],
     "answer": "coulomb’s law"},

    {"question": "What is the main role of tRNA during protein synthesis?",
     "choices": ["initiating transcription", "carrying amino acids to ribosomes", "encoding mRNA", "splicing introns"],
     "answer": "carrying amino acids to ribosomes"},

    {"question": "Which element is most commonly used as a neutron moderator in nuclear reactors?",
     "choices": ["carbon", "lead", "uranium", "heavy water"],
     "answer": "heavy water"},

    {"question": "What astronomical event is characterized by the collapse of a massive star’s core?",
     "choices": ["supernova", "quasar formation", "red shift", "black hole evaporation"],
     "answer": "supernova"},

    {"question": "Which part of the electromagnetic spectrum has the shortest wavelength?",
     "choices": ["visible light", "ultraviolet", "x-rays", "gamma rays"],
     "answer": "gamma rays"},

    {"question": "Which concept explains why a satellite stays in orbit instead of falling back to Earth?",
     "choices": ["inertia", "escape velocity", "centripetal acceleration", "free fall"],
     "answer": "free fall"},

    {"question": "What is the function of the enzyme helicase in DNA replication?",
     "choices": ["synthesizes rna primers", "breaks hydrogen bonds between base pairs", "joins okazaki fragments", "corrects replication errors"],
     "answer": "breaks hydrogen bonds between base pairs"},

    {"question": "Which chemical process is responsible for cellular energy production in the absence of oxygen?",
     "choices": ["photosynthesis", "lactic acid fermentation", "krebs cycle", "electron transport chain"],
     "answer": "lactic acid fermentation"},

    {"question": "Which thermodynamic law states that entropy of an isolated system always increases over time?",
     "choices": ["first law", "second law", "third law", "zeroth law"],
     "answer": "second law"},

    {"question": "Which quantum number determines the shape of an electron’s orbital?",
     "choices": ["principal 👎", "magnetic (m)", "spin (s)", "azimuthal (l)"],
     "answer": "azimuthal (l)"},

    {"question": "What is the term for the point directly above the focus of an earthquake on the Earth's surface?",
     "choices": ["hypocenter", "epicenter", "seismic node", "fault origin"],
     "answer": "epicenter"}
]

random.shuffle(question_bank)
class QuizApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Quiz App")
        self.window.geometry(f"{w}x{h}+0+0")
        self.window.config(bg="black")

        self.score = 0
        self.q_index = 0

        self.quest_lbl()
        self.load_question()

    def quest_lbl(self):
        questlblind_frm = Frame(self.window, width=20, height=10, bg="black")
        questlblind_frm.pack(pady=10)
        questlblind_frm.grid_propagate = (False)
        self.question_label = Label(questlblind_frm, text="", font=("sans-serif", 20, "bold"), bg="black", fg= "white")
        self.question_label.pack(pady=90)

        self.buttons = []
        for i in range(4):
            btn = Button(self.window, text="", command=lambda i=i: self.check_answer(i))
            btn.config(width=100,height=5, bg="#16404d",fg="#FCFBFC", font=("san-serif",15,"bold"))
            btn.pack(pady=5)
            self.buttons.append(btn)

    def load_question(self):
        question = question_bank[self.q_index]

        self.shuffled_choices = question["choices"][:]
        random.shuffle(self.shuffled_choices)

        self.question_label.config(text=question["question"])
        for i in range(4):
            self.buttons[i].config(text=self.shuffled_choices[i])
    

    def check_answer(self, index):
        selected = self.shuffled_choices[index]
        correct = question_bank[self.q_index]["answer"]

        if selected == correct:
            self.score += 1

        self.q_index += 1
        if self.q_index < len(question_bank):
            self.load_question()
        else:
            self.show_result()

    def show_result(self):
        self.question_label.destroy()
        for btn in self.buttons:
            btn.destroy()

        finalscore_label = Label(self.window, text=f"Score: {self.score} / {len(question_bank)}", font=("sans-serif", 24), bg = "black", fg = "white")
        finalscore_label.pack(pady=100)

app = QuizApp(quiz)
quiz.mainloop()
