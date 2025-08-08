from customtkinter import *
from CTkMessagebox import CTkMessagebox
import random
import sys

root = CTk()

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
     "choices" : ["principal (n)", "magnetic (m)", "spin (s)", "azimuthal (l)"], 
     "answer" : "azimuthal (l)"},

    {"question" : "What is the term for the point directly above the focus of an earthquake on the Earth's surface?", 
     "choices" : ["hypocenter", "epicenter", "seismic node", "fault origin"], 
     "answer" : "epicenter"}
]

class Quiz:
    def __init__(self, window, question_set):
        self.window = window
        self.question_set = question_set
        self.question_set_length = len(self.question_set)
        
        self.screen_height = self.window.winfo_screenheight()
        self.screen_width = self.window.winfo_screenwidth()
        self.window.geometry(f"{self.screen_width}x{self.screen_height}-7-5")
        self.window.title("Quiz App")
        self.window.resizable(False, False)
        
        self.text_font="Calibri"
        self.text_font_size=25
        self.button_font="Calibri"
        self.button_font_size=20
        
        self.question_count = 0
        self.score = 0
        self.buttons = ["button_1", "button_2", "button_3","button_4"]
        self.buttons_length = len(self.buttons)
        
        self.question_label = CTkLabel(master=self.window,
                                     font=(self.text_font, self.text_font_size, "bold"),
                                     wraplength=1000)
        self.question_remark_label = CTkLabel(master=self.window,
                                     font=(self.text_font, self.text_font_size, "bold"))
        self.question_count_label = CTkLabel(master=self.window,
                                     font=(self.text_font, self.text_font_size, "bold"))
        
        random.shuffle(self.question_set)
        self.shuffle()
        
    def shuffle(self):
        try:
            self.active_question = self.question_set[self.question_count]
            self.question = self.active_question["question"]
            self.choices = self.active_question["choices"]
            self.answer = self.active_question["answer"]
            random.shuffle(self.choices)
            
            self.initialize_ui()
        except Exception as error:
            self.show_error(error)
    
    def initialize_ui(self):
        try:
            self.question_label.configure(text=self.question)
            self.question_remark_label.configure(text=" ")
            self.question_count_label.configure(text=f"QUESTION {self.question_count + 1}")
            for index in range(self.buttons_length):
                self.buttons[index] = CTkButton(master=self.window,
                                                text=self.choices[index].upper(),
                                                width=800,
                                                height=70,
                                                state="normal",
                                                text_color="#ffffff",
                                                text_color_disabled="#ffffff",
                                                command= lambda indx = index : self.check_answer(indx),
                                                font=(self.button_font, self.button_font_size, "bold"))
                self.buttons[index].place(relx=0.5, rely=0.4 + (index*0.1), anchor="c")
            self.question_label.place(relx=0.5, rely=0.25, anchor="c")
            self.question_count_label.place(relx=0.08, rely=0.1)
        except Exception as error:
            self.show_error(error)
            
    def check_answer(self, button_index):
        if self.question_count >= self.question_set_length - 1:
            self.end_quiz()
            return 
        for index in range(self.buttons_length):
            self.buttons[index].configure(state="disabled")
        
        self.user_answer = self.buttons[button_index].cget("text")
        if self.user_answer.lower() == self.answer:
            self.score += 1
            self.question_remark_label.configure(text="CORRECT!", text_color="green")
            self.buttons[button_index].configure(fg_color="green", hover_color="green")
        else:
            self.question_remark_label.configure(text=f"INCORRECT! Answer is {self.answer.upper()}", text_color="yellow")
            self.buttons[button_index].configure(fg_color="red", hover_color="red")
        self.question_count += 1  
        self.question_remark_label.place(relx=0.5, rely=0.8, anchor="c")
        self.window.after(800, self.shuffle)          
            
    def end_quiz(self):
        self.score_percentage = int((self.score/self.question_set_length) * 100)
        self.remark = "Very Good!" if self.score_percentage > 90 else "Good!" if self.score_percentage > 60 else "Keep Practicing!" if self.score_percentage > 0 else "Try Again!"
        self.end_frame = CTkFrame(master=self.window,
                                  width=self.screen_width,
                                  height=self.screen_height)
        self.score_over = CTkLabel(master=self.end_frame,
                                   text=f"{self.score}/{self.question_set_length}",
                                   font=(self.text_font, 100, "bold"))
        self.score_percentage_label = CTkLabel(master=self.end_frame,
                                   text=f"{self.score_percentage}%",
                                   font=(self.text_font, 50, "bold"))
        self.score_remark = CTkLabel(master=self.end_frame,
                                   text=self.remark,
                                   font=(self.text_font, 30, "bold"))
        self.restart_button = CTkButton(master=self.end_frame,
                                        width=400,
                                        height=50,
                                        text="RESTART",
                                        font=(self.button_font, 17, "bold"),
                                        command=self.restart)
        self.end_frame.place(x=0,y=0)
        self.score_over.place(relx=0.5, rely=0.39, anchor="c")
        self.score_percentage_label.place(relx=0.5, rely=0.5, anchor="c")
        self.score_remark.place(relx=0.5, rely=0.57, anchor="c")
        self.restart_button.place(relx=0.5, rely=0.65, anchor="c")
        
    def restart(self):
        self.question_count = 0
        self.score = 0
        self.end_frame.place_forget()
        self.shuffle()
        
    def show_error(self, error):
        self.window.update()
        messagebox = CTkMessagebox(title="Application Error",
                                   message=error,
                                   icon="warning",
                                   option_1="OK")
        error_response = messagebox.get()
        if error_response == "OK":
            self.window.destroy()
            sys.exit()

if __name__ == "__main__":
    quiz = Quiz(root, question_bank)
    root.mainloop()