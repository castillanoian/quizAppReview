import customtkinter as ctk
import random
import re
import CTkMessagebox as CTkMessageBox
import sys

question_loc = "./question.txt"
with open(question_loc, "r") as file:
    questions = eval(file.read())
question_bank = questions

root = ctk.CTk()

TOTAL_QUESTIONS = 5
TOTAL_CHOICES = 4
standard_font = "Calibri"

class Quiz:
    def __init__(self, window, all_questions, total_questions=TOTAL_QUESTIONS):
        self.window = window
        self.all_questions = all_questions
        self.total_questions = total_questions
        self.question_count = 0
        self.score = 0
        
        sw, sh = window.winfo_screenwidth(), window.winfo_screenheight()
        ww, wh = int(sw * 0.8), int(sh * 0.8)
        x, y = (sw-ww)//2, (sh-wh)//5
        window.geometry(f"{ww}x{wh}+{x}+{y}")
        
        self.question_label = ctk.CTkLabel(window,
                                           font=(standard_font, 25, "bold"),
                                           wraplength=ww*0.7)
        self.question_count_label = ctk.CTkLabel(window,
                                                 font=(standard_font, 20, "bold"))
        self.question_remark_label = ctk.CTkLabel(window,
                                                 font=(standard_font, 18, "bold"))
        self.buttons = [ctk.CTkButton(window,
                                     width=800,
                                     height=60,
                                     font=(standard_font, 20, "bold"),
                                     text_color_disabled="#ffffff",
                                     command = lambda indx=i : self._check_multiple(indx)) for i in range(TOTAL_CHOICES)]
        self.entry = ctk.CTkEntry(self.window,
                                      width=550,
                                      height=50,
                                      font=(standard_font, 20, "bold"))
        self.entry_button = ctk.CTkButton(window,
                                          width=200,
                                          height=50,
                                          font=(standard_font, 20, "bold"),
                                          text="SUBMIT",
                                          command= self._check_fill)
        self.next_button = ctk.CTkButton(window,
                                     width=300,
                                     height=50,
                                     font=(standard_font, 20, "bold"),
                                     text ="NEXT QUESTION",
                                     command = self._next_question)
        self.score_label = ctk.CTkLabel(window,
                                           font=(standard_font, 100, "bold"),
                                           wraplength=ww*0.7)
        self.score_percentage_label = ctk.CTkLabel(window,
                                                 font=(standard_font, 50, "bold"))
        self.score_remark_label = ctk.CTkLabel(window,
                                                 font=(standard_font, 25, "bold"))
        self.restart_button = ctk.CTkButton(window,
                                     width=300,
                                     height=50,
                                     font=(standard_font, 20, "bold"),
                                     text ="RESTART",
                                     command = self._restart)
        self._start_quiz()
        
    @staticmethod
    def _normalize(text):
        return re.sub(r"[!@#$%^&*(){[]}\":;,<.>\?/]", "", re.sub(r"\s+", " ", text.strip().lower()))
        
    def _start_quiz(self):
        sample_size = min(len(self.all_questions), self.total_questions)
        self.question_set = random.sample(self.all_questions, sample_size)
        self._hide_widgets()
        self._show_questions()
        
    def _show_questions(self):
        if self.question_count >= len(self.question_set):
            self._end_quiz()
            return
        try: 
            current_question = self.question_set[self.question_count]
            self.current_answer = self._normalize(self.question_set[self.question_count]["answer"])
            self.question_label.configure(text=current_question["question"])
            self.question_count_label.configure(text=f"QUESTION {self.question_count + 1}/{len(self.question_set)}")
                
            self.question_label.place(relx=0.5,
                                        rely=0.28,
                                        anchor="c")
            self.question_count_label.place(relx=0.1,
                                        rely=0.1,
                                        anchor="c")
            
            if "choices" in current_question:
                choices = [self._normalize(choice) for choice in current_question["choices"]]
                self.correct_index = choices.index(self._normalize(self.current_answer))
                for i,btn in enumerate(self.buttons):
                    btn.configure(text=choices[i].upper(),
                                state="normal",
                                fg_color="#3B8ED0",
                                hover_color="#36719F",)
                    btn.place(relx=0.5,
                            rely = 0.4 + (i * 0.101),
                            anchor="c")
            else:
                self.entry = ctk.CTkEntry(self.window,
                                        width=550,
                                        height=50,
                                        font=(standard_font, 20, "bold"),
                                        placeholder_text="Enter Answer Here")
                self.entry.place(relx=0.4,
                                rely = 0.4,
                                anchor="c")
                self.entry_button.place(relx=0.75,
                                rely = 0.4,
                                anchor="c")
        except Exception as error:
            self._show_error(error)
            
    def _check_multiple(self, indx):
        for btns in self.buttons:
            btns.configure(state="disabled")
        
        if indx == self.correct_index:
            self.buttons[indx].configure(fg_color="green", hover_color="green")
            self.score += 1
            self.question_remark_label.configure(text="CORRECT!", text_color="green")
        else:
            self.buttons[indx].configure(fg_color="red", hover_color="red")
            self.question_remark_label.configure(text=f"INCORRECT! Answer is {self.current_answer.upper()}", text_color="yellow")
            
        self.buttons[self.correct_index].configure(fg_color="green", hover_color="green")
        self._show_interface_widgets()
    
    def _check_fill(self):
        if not self.entry.get():
            CTkMessageBox.CTkMessagebox(title="ENTRY ERROR",
                          message="Please Enter Your Answer")
            return
        if self._normalize(self.entry.get()) == self.current_answer:
            self.score += 1
            self.question_remark_label.configure(text="CORRECT!", text_color="green")
        else:
            self.question_remark_label.configure(text=f"INCORRECT! Answer is {self.current_answer.upper()}", text_color="yellow")
        self._show_interface_widgets()
        
    def _show_interface_widgets(self):
        self.question_remark_label.place(relx=0.5,
                               rely=0.8,
                               anchor="c")
        self.next_button.place(relx=0.5,
                               rely=0.9,
                               anchor="c")
    
    def _hide_widgets(self):
        for i in [self.entry, self.entry_button, self.next_button, self.question_remark_label, self.question_count_label, self.question_label,
                  self.score_label, self.score_percentage_label, self.score_remark_label, self.restart_button]:
            i.place_forget()
        for btn in self.buttons:
            btn.place_forget()
        
    def _next_question(self):
        self._hide_widgets()
        self.question_count += 1
        self._show_questions()

    def _end_quiz(self):
        self._hide_widgets()
        score_percentage = int((self.score/len(self.question_set)) * 100)
        remark, color = ("Very Good!", "green") if score_percentage > 90 else ("Good!", "blue") if score_percentage > 60 else ("You Did Okay!", "yellow") if score_percentage > 20 else ("Try Again!", "red")
        self.score_label.configure(text=f"{self.score}/{len(self.question_set)}")
        self.score_percentage_label.configure(text=f"{score_percentage}%")
        self.score_remark_label.configure(text=remark, text_color=color)
        
        self.score_label.place(relx=0.5,
                               rely=0.4,
                               anchor="c")
        self.score_percentage_label.place(relx=0.5,
                               rely=0.55,
                               anchor="c")
        self.score_remark_label.place(relx=0.5,
                               rely=0.65,
                               anchor="c")
        self.restart_button.place(relx=0.5,
                               rely=0.75,
                               anchor="c")
    def _restart(self):
        self.score = 0
        self.question_count = 0
        self._start_quiz()
        
    def _show_error(self, error):
        message = CTkMessageBox.CTkMessagebox(title="APPLICATION ERROR",
                                              message=error,
                                              icon="warning",
                                              option_1="OK")
        if message.get() == "OK":
            sys.exit()

if __name__ == "__main__":
    quiz = Quiz(root, question_bank)
    root.mainloop()  