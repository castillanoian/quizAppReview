from tkinter import *
import random

question_bank = [
    {"question" : "Which fundamental interaction is responsible for beta decay in radioactive atoms?", 
     "choices" : ["strong force", "electromagnetic force", "weak nuclear force", "gravitational force"], 
     "answer" : "weak nuclear force"},

    {"question" : "What structure in eukaryotic cells is primarily responsible for modifying, sorting, and packaging proteins?", 
     "choices" : ["lysosome", "golgi apparatus", "endoplasmic reticulum", "nucleolus"], 
     "answer" : "golgi apparatus"},

    {"question" : "Which principle states that the position and momentum of a particle cannot both be precisely determined at the same time?", 
     "choices" : ["pauli exclusion principle", "uncertainty principle", "superposition principle", "complementarity principle"], 
     "answer" : "uncertainty principle"},

    {"question" : "Which geological process is primarily responsible for the creation of mountain ranges like the Himalayas?", 
     "choices" : ["volcanism", "plate subduction", "seafloor spreading", "continental collision"], 
     "answer" : "continental collision"},

    {"question" : "Which law quantifies the force between two point ch-arges?", 
     "choices" : ["newton’s third law", "coulomb’s law", "ohm’s law", "faraday’s law"], 
     "answer" : "coulomb’s law"},

    {"question" : "What is the main role of tRNA during protein synthesis?", 
     "choices" : ["initiating transcription", "carrying amino acids to ribosomes", "encoding mRNA", "splicing introns"], 
     "answer" : "carrying amino acids to ribosomes"},

    {"question" : "Which element is most commonly used as a neutron moderator in nuclear reactors?", 
     "choices" : ["carbon", "lead", "uranium", "heavy water"], 
     "answer" : "heavy water"},

    {"question" : "What astronomical event is characterized by the collapse of a massive star’s core?", 
     "choices" : ["supernova", "quasar formation", "red shift", "black hole evaporation"], 
     "answer" : "supernova"},

    {"question" : "Which part of the electromagnetic spectrum has the shortest wavelength?", 
     "choices" : ["visible light", "ultraviolet", "x-rays", "gamma rays"], 
     "answer" : "gamma rays"},

    {"question" : "Which concept explains why a satellite stays in orbit instead of falling back to Earth?", 
     "choices" : ["inertia", "escape velocity", "centripetal acceleration", "free fall"], 
     "answer" : "free fall"},

    {"question" : "What is the function of the enzyme helicase in DNA replication?", 
     "choices" : ["synthesizes rna primers", "breaks hydrogen bonds between base pairs", "joins okazaki fragments", "corrects replication errors"], 
     "answer" : "breaks hydrogen bonds between base pairs"},

    {"question" : "Which chemical process is responsible for cellular energy production in the absence of oxygen?", 
     "choices" : ["photosynthesis", "lactic acid fermentation", "krebs cycle", "electron transport chain"], 
     "answer" : "lactic acid fermentation"},

    {"question" : "Which thermodynamic law states that entropy of an isolated system always increases over time?", 
     "choices" : ["first law", "second law", "third law", "zeroth law"], 
     "answer" : "second law"},

    {"question" : "Which quantum number determines the shape of an electron’s orbital?", 
     "choices" : ["principal (p)", "magnetic (m)", "spin (s)", "azimuthal (l)"], 
     "answer" : "azimuthal (l)"},

    {"question" : "What is the term for the point directly above the focus of an earthquake on the Earth's surface?", 
     "choices" : ["hypocenter", "epicenter", "seismic node", "fault origin"], 
     "answer" : "epicenter"}
]

random.shuffle(question_bank)

root = Tk()

class Quiz:
    def __init__(self, window):
        self.window = window
        window.state('zoomed')
        window.config(bg="#262626")
        self.question_index = 0
        self.current_item = 1
        self.correct = 0
        self.choice = ["choice1", "choice2", "choice3", "choice4"]


        self.load_page()
        self.load_item()
        
    def load_page(self):
        self.label_frame = Frame(self.window, bg="#262626")
        self.choices_frame = Frame(self.window, bg="#262626")

        self.item_label = Label(self.label_frame, text=f"Question {self.current_item}", font="Arial, 20", fg="white", bg="#262626")
        self.question_label = Label(self.label_frame, text="test", font="Arial, 20", fg="white", bg="#262626")
        
        for i in range(len(self.choice)):
            self.choice[i] = Button(self.choices_frame, height=1, width=40, font="Arial, 30", command=lambda x=i: self.on_click(question_bank[self.question_index]["choices"][x], self.choice[x]), bg="white")
            self.choice[i].grid(row=0+i, column=0, padx=20, pady=10)
        
        self.label_frame.pack(pady=(50, 0))
        self.choices_frame.pack()
        self.item_label.pack()
        self.question_label.pack(pady=30)

    def load_item(self):
        random.shuffle(question_bank[self.question_index]["choices"])
        self.item_label.config(text=f"Question {self.current_item}")
        self.question_label.config(text=question_bank[self.question_index]["question"])

        for i in range(len(self.choice)):
            self.choice[i].config(text=question_bank[self.question_index]["choices"][i])
        

    def next_item(self, element):
        self.check_label.destroy()
        self.show_answer.destroy()

        for i in range(len(self.choice)):
            self.choice[i].config(state="normal")
        
        element.config(bg="white")

        if self.question_index < len(question_bank):
            self.load_item()
        else:
            self.end()
    
    def on_click(self, choosen, element):
        for i in range(len(self.choice)):
            self.choice[i].config(state="disabled")
        
        self.check_label = Label(self.window, text="", bg="#262626", font="Arial, 40")
        self.show_answer = Label(self.window, text="", bg="#262626", fg="yellow", font="Arial, 30")
        self.check_label.pack(pady=(20, 0))
        self.show_answer.pack()

        if choosen == question_bank[self.question_index]["answer"]:
            self.correct += 1
            element.config(bg="green")
            self.check_label.config(text="Correct!", fg="green")
        else:
            element.config(bg="red")
            self.check_label.config(text="Incorrect!", fg="red")
            self.show_answer.config(text=f"The answer is: {question_bank[self.question_index]["answer"]}")

        self.window.after(2000, lambda: (element.config(bg="white"), self.next_item(element)))

        self.question_index += 1
        self.current_item += 1

    def end(self):
        self.label_frame.destroy()
        self.choices_frame.destroy()

        self.percentage = int(self.correct/len(question_bank)*100)

        self.result_frame = Frame(self.window, bg="#262626")
        self.feedback_label = Label(self.result_frame, bg="#262626", fg="white", font="Arial, 50")
        self.score_percentage = Label(self.result_frame, text=f"{self.percentage}% Score", bg="#262626", fg="white", font="Arial, 40")
        self.out_of_items = Label(self.result_frame, text=f"{self.correct}/{len(question_bank)}", bg="#262626", fg="white", font="Arial, 30")
        self.restart_btn = Button(self.result_frame, text="Restart", command=self.restart, font="Arial, 20")

        if self.percentage == 100:
            self.feedback = "Perfect!"
        elif 80 < self.percentage != 100:
            self.feedback = "Good Job!"
        elif 50 < self.percentage < 80:
            self.feedback = "Not Bad"
        elif 10 < self.percentage < 50:
            self.feedback = "Meh"
        else:
            self.feedback = "Atleast you tried :)"
        self.feedback_label.config(text=self.feedback)
        
        self.result_frame.pack(pady=(200, 0))
        self.feedback_label.pack()
        self.score_percentage.pack()
        self.out_of_items.pack()
        self.restart_btn.pack()

    def restart(self):
        random.shuffle(question_bank)
        self.result_frame.destroy()

        self.question_index = 0
        self.current_item = 1
        self.correct = 0
        
        self.load_page()
        self.load_item()  

app = Quiz(root)
root.mainloop()