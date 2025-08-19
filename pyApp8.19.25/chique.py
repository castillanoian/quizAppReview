import customtkinter as ctk
import re
import sys
import random
import CTkMessagebox as ctkmessagebox

question_path = "./question.txt"
with open(question_path, "r") as file:
    question_bank = eval(file.read())
    
root = ctk.CTk()

TOTAL_QUESTIONS = 3
TOTAL_CHOICES = 4
STANDARD_FONT = "Calibri"
BACKGROUND_COLOR = "#0F0F0F"
    
class Quiz:
    def __init__(self, window, all_questions, total_questions=TOTAL_QUESTIONS):
        self.window = window
        self.all_questions = all_questions
        self.total_questions = total_questions
        self.score = 0
        self.question_count = 0
        self.used_questions = []
        
        sw, sh = window.winfo_screenwidth(), window.winfo_screenheight()
        ww, wh = int(sw * 0.8), int(sh * 0.8)
        x, y = ((sw - ww) // 2), ((sh - wh) // 2)
        window.geometry(f"{ww}x{wh}+{x}+{y}")
        window.title("QUIZ APP")
        window.configure(fg_color=BACKGROUND_COLOR)
        
        self.question_frame = ctk.CTkFrame(window, 
                                           width=ww,
                                           height=wh,
                                           fg_color=BACKGROUND_COLOR)
        self.question_label = ctk.CTkLabel(self.question_frame,
                                           font=(STANDARD_FONT, 25, "bold"),
                                           wraplength=int(ww*0.9))
        self.question_count_label = ctk.CTkLabel(self.question_frame,
                                           font=(STANDARD_FONT, 18, "bold"))
        self.question_remark_label = ctk.CTkLabel(self.question_frame,
                                           font=(STANDARD_FONT, 20, "bold"))
        self.buttons = [ctk.CTkButton(self.question_frame,
                                      width=800,
                                      height=65,
                                      font=(STANDARD_FONT, 20, "bold"),
                                      command= lambda indx = i : self._check_multiple(indx)) for i in range(TOTAL_CHOICES)]     
        
        
        self.entry_buttton = ctk.CTkButton(self.question_frame,
                                           width=200,
                                           height=55,
                                           text="SUBMIT",
                                           font=(STANDARD_FONT, 20, "bold"),
                                           command= self._check_fill)   
        self.next_button = ctk.CTkButton(self.question_frame,
                                         width=300,
                                         height=45,
                                         text="NEXT QUESTION",
                                         font=(STANDARD_FONT, 15, "bold"),
                                         command=self._next_question)
        self.score_frame = ctk.CTkFrame(window,
                                        width=ww,
                                        height=wh,
                                        fg_color=BACKGROUND_COLOR)
        self.restart_button = ctk.CTkButton(self.score_frame,
                                         width=300,
                                         height=40,
                                         text="RESTART",
                                         font=(STANDARD_FONT, 20, "bold"),
                                         command=self._restart_quiz)
        self.review_box = ctk.CTkScrollableFrame(self.score_frame, 
                                                 width=800,
                                                 height=350,
                                                 fg_color=BACKGROUND_COLOR,
                                                 label_text="Question Review")
        self.score_label = ctk.CTkLabel(self.score_frame,
                                           font=(STANDARD_FONT, 50, "bold"))
        self.score_remark_label = ctk.CTkLabel(self.score_frame,
                                           font=(STANDARD_FONT, 25, "bold"))
        
        
        
        self.question_label.place(relx=0.5, rely=0.29, anchor="c")
        self.question_count_label.place(relx=0.07, rely=0.09, anchor="c")
        
        self.score_label.place(relx=0.5, rely=0.12, anchor="c")
        self.score_remark_label.place(relx=0.5, rely=0.2, anchor="c")
        self.restart_button.place(relx=0.5, rely=0.27, anchor="c")
        self.review_box.place(relx=0.5, rely=0.65, anchor="c")
        self._start_quiz()
        
    @staticmethod
    def _normalize(text):
        return re.sub(r"[!@#$%^&*(){{}}]\"\?./<>,;:", "", re.sub(r"\s+", " ", text.strip().lower()))
    
    @staticmethod
    def _show_error(error):
        error_message =ctkmessagebox.CTkMessagebox(title="Application Error",
                                    message=error,
                                    option_1="OK")
        if error_message.get() == "OK":
            sys.exit()
        
    def _start_quiz(self):
        sample_size = min(len(self.all_questions), self.total_questions)
        self.question_set = random.sample(self.all_questions, sample_size)
        self._show_quiz_widgets()
     
    def _show_quiz_widgets(self):
        if self.question_count >= len(self.question_set):
            self._end_quiz()
            return
        self.active_set = self.question_set[self.question_count]
        self.current_question = self.question_set[self.question_count]["question"]
        self.current_answer = self._normalize(self.question_set[self.question_count]["answer"])
        
        self.question_frame.place(relx=0.5, rely=0.5, anchor="c")
        self.question_label.configure(text=self.current_question)
        self.question_count_label.configure(text=f"QUESTION {self.question_count+1}/{len(self.question_set)}")
        
        self.entry = ctk.CTkEntry(self.question_frame,
                                  width=600,
                                  height=55,
                                  placeholder_text="Enter Your Answer Here",
                                  font=(STANDARD_FONT, 20, "bold"))
        
        if "choices" in self.active_set:
            self.choices = [self._normalize(choices) for choices in self.active_set["choices"]]
            random.shuffle(self.choices)
            self.correct_index = self.choices.index(self.current_answer)
            for i,btn in enumerate(self.buttons):
                btn.configure(text=self.choices[i].upper(),
                              state="normal",
                              text_color="#ffffff",
                              text_color_disabled="#ffffff",
                              hover_color="#07495e",
                              fg_color="#36719F")
                btn.place(relx=0.5, rely = 0.41 + (i * 0.109), anchor="c")
        else:
            self.entry.place(relx=0.42, rely = 0.4, anchor="c")
            self.entry_buttton.place(relx=0.79, rely = 0.4, anchor="c")
            
    def _show_interface_widgets(self):
        self.question_remark_label.place(relx=0.5, rely=0.86, anchor="c")
        self.next_button.place(relx=0.5, rely=0.93, anchor="c")
    
    def _next_question(self):
        self.question_count+=1
        self._hide_widgets()
        self._show_quiz_widgets()
    
    def _hide_widgets(self):
        for i in [self.entry, self.entry_buttton, self.next_button, self.question_remark_label]:
            i.place_forget()
        for i in self.buttons:
            i.place_forget()
        
    def _check_multiple(self, index):
        for i in self.buttons:
            i.configure(state="disabled")
            
        self.buttons[self.correct_index].configure(fg_color="green", hover_color="green")
        if index == self.correct_index:
            self.score+=1
            self.question_remark_label.configure(text="CORRECT!", text_color="green")
        else:
            self.buttons[index].configure(fg_color="red", hover_color="red",)
            self.question_remark_label.configure(text=f"INCORRECT! Answer is {self.current_answer.upper()}", text_color="yellow")
        
        self._append_used_question(self.choices[index])
        self._show_interface_widgets()
        
    def _check_fill(self):
        user_answer = self.entry.get()
        
        if not user_answer:
            ctkmessagebox.CTkMessagebox(title="Entry Error",
                                        message="No Answer Found. Please Enter Your Answer")
            return
        if self._normalize(user_answer) == self.current_answer:
            self.question_remark_label.configure(text="CORRECT!", text_color="green")
            self.score+=1
        else:
            self.question_remark_label.configure(text=f"INCORRECT! Answer is {self.current_answer.upper()}", text_color="yellow")
        self._append_used_question(user_answer)
        self._show_interface_widgets()
        
    def _append_used_question(self, user_answer):
        self.used_questions.append({"question": self.current_question,
                                    "user_answer": user_answer,
                                    "answer": self.current_answer})
        
    def _end_quiz(self):
        self.question_frame.place_forget()
        score_percentage = int((self.score/len(self.question_set))*100)
        remark, color = ("Very Good!", "green") if score_percentage > 90 else ("Good!", "blue") if score_percentage > 50 else ("Try Again!", "yellow") if score_percentage > 5 else ("You did your best!", "red")
        self.score_label.configure(text=f"{self.score}/{len(self.question_set)} with {score_percentage}% Accuracy")
        self.score_remark_label.configure(text=remark, text_color=color)
        self.score_frame.place(relx=0.5, rely=0.5, anchor="c")
        self.frames = [ctk.CTkFrame(self.review_box,
                                   border_width=1,       # thickness
                                   border_color="#757575",
                                   width=800,
                                   height=200,) for p in range(len(self.used_questions))]
        for i,items in enumerate(self.used_questions):
            
            items["question"] = ctk.CTkLabel(self.frames[i],
                                 text=f"{items["question"]}",
                                 font=(STANDARD_FONT, 20, "bold"),
                                 wraplength=700)
            items["user_answer"] = ctk.CTkLabel(self.frames[i],
                                 text=f"Your Answer: {items["user_answer"].capitalize()}",
                                 font=(STANDARD_FONT, 20, "bold"),
                                 text_color= "green" if items["user_answer"].lower() == items["answer"].lower() else "yellow",
                                 wraplength=700)
            items["answer"] = ctk.CTkLabel(self.frames[i],
                                 text=f"Correct Answer: {items["answer"].capitalize()}",
                                 font=(STANDARD_FONT, 20, "bold"),
                                 text_color= "green",
                                 wraplength=700)
            self.frames[i].pack_propagate(False) 
            self.frames[i].pack(pady=5)
            items["question"] .pack(pady=(30,5))
            items["user_answer"] .pack(pady=0)
            items["answer"] .pack(pady=0)
        
    def _restart_quiz(self):
        for i in self.frames:
            i.destroy()
        self.used_questions.clear()
        self.score_frame.place_forget()
        self.score = 0
        self.question_count = 0
        self.question_frame.place(relx=0.5, rely=0.5, anchor="c")
        self._start_quiz()
        
if __name__ == "__main__":
    quiz = Quiz(root, question_bank)
    root.mainloop()
    