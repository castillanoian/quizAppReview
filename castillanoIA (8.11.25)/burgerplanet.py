import customtkinter as ctk
import re
import random
from CTkMessagebox import CTkMessagebox
import sys

question_path = "./question.txt"
with open(question_path, "r") as file:
    questions = eval(file.read()) 
question_bank = questions

"<--WINDOW-->"
root = ctk.CTk()
"""<--CONSTANTS-->"""

QUESTION_TEXT_FONT = ("Calibri", 25, "bold")
QUESTION_COUNT_FONT = ("Calibri", 20, "bold")
QUESTION_REMARK_FONT = ("Calibri", 22, "bold")
SCORE_OVER_FONT = ("Calibri", 100, "bold")
SCORE_PERCENTAGE_FONT = ("Calibri", 50, "bold")
SCORE_REMARK_FONT = ("Calibri", 30, "bold")
CHOICES_BUTTON_FONT = ("Calibri", 20, "bold")
ENTRY_FONT = ("Calibri", 20, "bold")
RESTART_BUTTON_FONT = ("Calibri", 17, "bold")
NEXT_BUTTON_FONT = ("Calibri", 15, "bold")

CHOICES_BUTTON_WIDTH = 800
CHOICES_BUTTON_HEIGHT = 60
NEXT_BUTTON_WIDTH = 300
NEXT_BUTTON_HEIGHT = 50
ENTRY_WIDTH = 600
ENTRY_HEIGHT = 60
SUBMIT_BUTTON_WIDTH = 200
SUBMIT_BUTTON_HEIGHT = 60
RESTART_BUTTON_WIDTH = 180
RESTART_BUTTON_HEIGHT = 50


CORRECT_COLOR = "green"
INCORRECT_COLOR = "red"
CORRECT_REMARK_COLOR = "green"
INCORRECT_REMARK_COLOR = "yellow"
BUTTON_FG_COLOR = "#3498DB"
BUTTON_HOVER_COLOR = "#2980B9" 
BUTTON_TEXT_COLOR = "#ffffff"
BUTTON_TEXT_COLOR_DISABLED = "#ffffff"
MAX_CHOICES = 4
TOTAL_QUESTIONS = 10

"""<--CLASS-->"""
class Quiz:
    def __init__(self, window, all_questions):
        self.window = window
        self.all_questions = all_questions
        self.question_set = []
        
        self.question_count = 0
        self.score = 0
        
        self.layout_config = {}
        self.question_data = {}
        
        self.question_label = None
        self.question_count_label = None
        self.question_remark_label = None
        self.score_label = None
        self.score_percentage_label = None
        self.score_remark_label = None
        self.entry = None
        self.next_button = None
        self.submit_entry_button = None
        self.restart_button = None
        self.buttons = []
        
        self._initialize_window()
        self._create_widgets()
        self._start_quiz()
    
    def _initialize_window(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.85)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 5
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.title("QUIZ APP")
        
        self.layout_config = {
            "standard_relx" : 0.5,
            "standard_anchor" : "c",
            "question_label_relx" : 0.5,
            "question_label_rely" : 0.25,
            "question_count_relx" : 0.08,
            "question_count_rely" : 0.1,
            "question_remark_relx" : 0.5,
            "question_remark_rely" : 0.8,
            "initial_choices_button_rely" : 0.38,
            "choices_button_spacing" : 0.097,
            "entry_relx" : 0.4,
            "entry_rely" : 0.45,
            "next_button_relx" : 0.5,
            "next_button_rely" : 0.9,
            "submit_button_relx" : 0.77,
            "submit_button_rely" : 0.45,
            "wraplength" : window_width * 0.7,
            "score_relx" : 0.5,
            "score_rely" : 0.35,
            "score_percentage_relx" : 0.5,
            "score_percentage_rely" : 0.5,
            "score_remark_relx" : 0.5,
            "score_remark_rely" : 0.6,
            "restart_button_relx" : 0.5,
            "restart_button_rely" : 0.68,
        }
        
    def _create_widgets(self):
        self.question_label = ctk.CTkLabel(master=self.window,
                                      font=QUESTION_TEXT_FONT,
                                      wraplength=self.layout_config["wraplength"])
        self.question_count_label = ctk.CTkLabel(master=self.window,
                                                  font=QUESTION_COUNT_FONT)
        self.question_remark_label= ctk.CTkLabel(master=self.window,
                                                 font=QUESTION_REMARK_FONT)
        self.next_button = ctk.CTkButton(master=self.window,
                                       width=NEXT_BUTTON_WIDTH,
                                       height=NEXT_BUTTON_HEIGHT,
                                       text="NEXT",
                                       font=NEXT_BUTTON_FONT,
                                       command=self._proceed_next_question)
        self.submit_entry_button = ctk.CTkButton(master=self.window,
                                       width=SUBMIT_BUTTON_WIDTH,
                                       height=SUBMIT_BUTTON_HEIGHT,
                                       text="SUBMIT",
                                       font=NEXT_BUTTON_FONT,
                                       command=self._check_entry_answer)
        self.restart_button = ctk.CTkButton(master=self.window,
                                       width=RESTART_BUTTON_WIDTH,
                                       height=RESTART_BUTTON_HEIGHT,
                                       text="RESTART",
                                       font=RESTART_BUTTON_FONT,
                                       command=self._retsart)
        
        self.buttons = [ctk.CTkButton(master=self.window,
                                      width=CHOICES_BUTTON_WIDTH,
                                      height=CHOICES_BUTTON_HEIGHT,
                                      font=CHOICES_BUTTON_FONT,
                                      text="",
                                      state="normal",
                                      fg_color=BUTTON_FG_COLOR,
                                      hover_color=BUTTON_HOVER_COLOR,
                                      text_color=BUTTON_TEXT_COLOR,
                                      text_color_disabled=BUTTON_TEXT_COLOR_DISABLED,
                                      command=lambda index=idx: self._check_choices_answer(index)) for idx in range(MAX_CHOICES)]
        self.entry = ctk.CTkEntry(master=self.window,
                                  width=ENTRY_WIDTH,
                                  height=ENTRY_HEIGHT,
                                  font=ENTRY_FONT)   
        self.score_label = ctk.CTkLabel(master=self.window,
                                        font=SCORE_OVER_FONT)
        self.score_percentage_label = ctk.CTkLabel(master=self.window,
                                                   font=SCORE_PERCENTAGE_FONT) 
        self.score_remark_label = ctk.CTkLabel(master=self.window,
                                              font=SCORE_REMARK_FONT) 
    @staticmethod
    def normalizer(text):
        normalized_text = re.sub(r"\s+", " ", text.strip().lower())
        return re.sub("[!@#$%^&*();:\"'{[]},<.>/?]", "", normalized_text)
    
    def _select_question(self):
        sample_size = min(len(self.all_questions), TOTAL_QUESTIONS)  
        if len(self.all_questions) > 1000:
            indices = random.sample(len(self.all_questions), sample_size)
            self.question_set = [self.all_questions[i] for i in indices]
        else:
            self.question_set = random.sample(self.all_questions, sample_size)
            
    def _determine_question_type(self, question_data):
        if "choices" not in question_data:
            return "fill_blank"
        return "multiple_choice"        
        
    def _intialize_question_data(self):
        active_question = self.question_set[self.question_count]  
        question_type = self._determine_question_type(active_question)
        
        self.question_data = {
            "question_text" : active_question["question"],
            "type" : question_type,
            "answer" : self.normalizer(active_question["answer"])
        }
                
        if question_type == "multiple_choice":
            choices = active_question["choices"]
            choice_list = [self.normalizer(choices[i]) for i in range(len(choices))]
            
            correct_index = -1
            for i in range(len(choice_list)):
                if choice_list[i] == self.question_data["answer"]:
                    correct_index = i
                    break
            
            self.question_data.update({
                "choices" : choice_list,
                "correct_index" : correct_index
            })
            

    def _show_question(self):
        if self.question_count >= len(self.question_set):
            self._end_quiz()
            return
        try: 
            self._intialize_question_data()
            self.question_remark_label.configure(text=" ")
            self.question_count_label.configure(text=f"QUESTION {self.question_count+1}/{len(self.question_set)}")
            self.question_label.configure(text=self.question_data["question_text"])
            self.entry.configure(state="normal")
        
            if self.question_data["type"] == "multiple_choice":
                self._show_multiple_choice()
            else:
                self._show_fill_blank()  
                
            self.question_label.place(relx=self.layout_config["question_label_relx"],
                                    rely=self.layout_config["question_label_rely"],
                                    anchor=self.layout_config["standard_anchor"])  
            self.question_count_label.place(relx=self.layout_config["question_count_relx"],
                                    rely=self.layout_config["question_count_rely"],
                                    anchor=self.layout_config["standard_anchor"])
        except Exception as error:
            self._show_error(f"@def_show_question: {error}")
    
    def _show_multiple_choice(self):
        for i, btn in enumerate(self.buttons):
            btn.configure(text=self.question_data["choices"][i].upper(),
                          state="normal",
                          fg_color=BUTTON_FG_COLOR,
                          hover_color=BUTTON_HOVER_COLOR,
                          text_color=BUTTON_TEXT_COLOR,)
            btn.place(relx=self.layout_config["standard_relx"],
                      rely = self.layout_config["initial_choices_button_rely"] + (i * self.layout_config["choices_button_spacing"]),
                      anchor=self.layout_config["standard_anchor"])
            
    def _show_fill_blank(self):
        self.entry.delete(0, "end")
        self.entry.place(relx=self.layout_config["entry_relx"],
                         rely=self.layout_config["entry_rely"],
                         anchor=self.layout_config["standard_anchor"])
        self.submit_entry_button.place(relx=self.layout_config["submit_button_relx"],
                                       rely=self.layout_config["submit_button_rely"],
                                       anchor=self.layout_config["standard_anchor"])
        
    def _initialize_interface_buttons(self):
        self.next_button.place(relx=self.layout_config["next_button_relx"],
                         rely=self.layout_config["next_button_rely"],
                         anchor=self.layout_config["standard_anchor"])
        self.question_remark_label.place(relx=self.layout_config["question_remark_relx"],
                                        rely=self.layout_config["question_remark_rely"],
                                        anchor=self.layout_config["standard_anchor"])
        
    def _check_choices_answer(self, index):
        correct_index = self.question_data["correct_index"]
        for btn in self.buttons:
            btn.configure(state="disabled")
        if index == correct_index:
            self.buttons[index].configure(fg_color=CORRECT_COLOR,
                                          hover_color=CORRECT_COLOR)
            self.score += 1
            self.question_remark_label.configure(text="CORRECT!",
                                                 text_color=CORRECT_REMARK_COLOR)
        else:
            self.buttons[index].configure(fg_color=INCORRECT_COLOR,
                                          hover_color=INCORRECT_COLOR)
            self.question_remark_label.configure(text=f"INCORRECT! Answer is {self.question_data["answer"].upper()}",
                                                 text_color=INCORRECT_REMARK_COLOR)
        self.buttons[correct_index].configure(fg_color=CORRECT_COLOR,
                                          hover_color=CORRECT_COLOR)
        self._initialize_interface_buttons()
        
    def _check_entry_answer(self):
        user_answer = self.entry.get()
        if not user_answer:
            CTkMessagebox(title="ENTRY ERROR",
                          message="Entry is Empty. Please Input Your Answer")
            return
        user_answer = self.normalizer(user_answer)
        self.entry.configure(state="disabled")
        
        if user_answer == self.question_data["answer"]:
            self.score += 1
            self.question_remark_label.configure(text="CORRECT!",
                                                 text_color=CORRECT_REMARK_COLOR)
        else:
            self.question_remark_label.configure(text=f"INCORRECT! Answer is {self.question_data["answer"].upper()}",
                                                 text_color=INCORRECT_REMARK_COLOR)
        self._initialize_interface_buttons()
        
    def _proceed_next_question(self):
        self.question_count += 1
        self._hide_selection_widgets()
        self._show_question()
        
    def _hide_selection_widgets(self):
        for btn in self.buttons:
            btn.place_forget()
        self.entry.place_forget()
        self.question_remark_label.place_forget()
        self.question_label.place_forget()
        self.question_count_label.place_forget()
        self.next_button.place_forget()
        self.submit_entry_button.place_forget()
                    
    def _start_quiz(self):
        try:
            self._select_question()
            self._show_question()
        except Exception as error:
            self._show_error(error)
            
    def _end_quiz(self):
        score_percentage = int((self.score/len(self.question_set)*100))
        remark, color = self._remark_and_color(score_percentage)
        self._hide_selection_widgets()   
        self.score_label.configure(text=f"{self.score}/{len(self.question_set)}")
        self.score_percentage_label.configure(text=f"{score_percentage}%")
        self.score_remark_label.configure(text=remark,
                                          text_color=color)
        
        self.score_label.place(relx=self.layout_config["score_relx"],
                               rely=self.layout_config["score_rely"],
                               anchor=self.layout_config["standard_anchor"])
        self.score_percentage_label.place(relx=self.layout_config["score_percentage_relx"],
                               rely=self.layout_config["score_percentage_rely"],
                               anchor=self.layout_config["standard_anchor"])
        self.score_remark_label.place(relx=self.layout_config["score_remark_relx"],
                               rely=self.layout_config["score_remark_rely"],
                               anchor=self.layout_config["standard_anchor"])
        self.restart_button.place(relx=self.layout_config["restart_button_relx"],
                               rely=self.layout_config["restart_button_rely"],
                               anchor=self.layout_config["standard_anchor"])
        
    def _remark_and_color(self, score_percentage):
        if score_percentage > 90:
            return "Very Good!", "green"
        elif score_percentage > 60:
            return "Good!", "blue"
        else:
            return "Keep Practicing!", "red"  
    def _retsart(self):
        self.score_label.place_forget()
        self.score_percentage_label.place_forget()
        self.score_remark_label.place_forget()
        self.restart_button.place_forget()
        self.question_count = 0
        self.score = 0
        
        self._initialize_window()
        self._create_widgets()
        self._start_quiz()
        
        
    def _show_error(self, error):
        error_message = CTkMessagebox(title="APPLICATION ERROR", 
                                      message=error,
                                      option_1="OK")
        if error_message.get() == "OK":
            self.window.destroy()
            sys.exit()
        

if __name__ == "__main__":
    quiz = Quiz(root, question_bank)
    root.mainloop()