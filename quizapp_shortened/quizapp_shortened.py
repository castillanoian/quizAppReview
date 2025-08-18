import customtkinter as ctk
import re
import random
from CTkMessagebox import CTkMessagebox
import sys

# Load questions
with open("./question.txt", "r") as file:
    question_bank = eval(file.read())

# CONFIGURABLE VARIABLES
TOTAL_QUESTIONS = 10  # Change this to adjust quiz length


class Quiz:
    def __init__(self, window, all_questions, num_questions=TOTAL_QUESTIONS):
        self.window = window
        self.all_questions = all_questions
        self.num_questions = num_questions  # Store the number of questions for this quiz
        self.question_count = 0
        self.score = 0

        # Setup window
        sw, sh = window.winfo_screenwidth(), window.winfo_screenheight()
        ww, wh = int(sw * 0.8), int(sh * 0.85)
        window.geometry(f"{ww}x{wh}+{(sw - ww) // 2}+{(sh - wh) // 5}")
        window.title("QUIZ APP")

        # Create top-right restart button (always visible)
        self.top_restart_btn = ctk.CTkButton(
            window, width=120, height=35, text="RESTART",
            font=("Calibri", 14, "bold"), command=self._restart
        )
        self.top_restart_btn.place(relx=0.98, rely=0.05, anchor="e")

        # Existing widgets
        self.question_label = ctk.CTkLabel(window, font=("Calibri", 25, "bold"), wraplength=ww * 0.7)
        self.count_label = ctk.CTkLabel(window, font=("Calibri", 20, "bold"))
        self.remark_label = ctk.CTkLabel(window, font=("Calibri", 22, "bold"))
        self.next_btn = ctk.CTkButton(window, width=300, height=50, text="NEXT",
                                      font=("Calibri", 15, "bold"), command=self._next_question)

        self.buttons = [ctk.CTkButton(window, width=800, height=60, font=("Calibri", 20, "bold"),
                                      fg_color="#3498DB", hover_color="#2980B9", text_color="white",
                                      command=lambda i=idx: self._check_choice(i)) for idx in range(4)]

        self.entry = ctk.CTkEntry(window, width=600, height=60, font=("Calibri", 20, "bold"), placeholder_text=".........")
        self.submit_btn = ctk.CTkButton(window, width=200, height=60, text="SUBMIT",
                                        font=("Calibri", 15, "bold"), command=self._check_entry)

        self.score_label = ctk.CTkLabel(window, font=("Calibri", 100, "bold"))
        self.percent_label = ctk.CTkLabel(window, font=("Calibri", 50, "bold"))
        self.final_remark = ctk.CTkLabel(window, font=("Calibri", 30, "bold"))
        self.restart_btn = ctk.CTkButton(window, width=180, height=50, text="RESTART",
                                         font=("Calibri", 17, "bold"), command=self._restart)

        self._start_quiz()

    @staticmethod
    def _normalize(text):
        return re.sub(r"[!@#$%^&*();:\"'{[]},<.>/?]", "", re.sub(r"\s+", " ", text.strip().lower()))

    def _start_quiz(self):
        # Select random questions using the configurable variable
        sample_size = min(len(self.all_questions), self.num_questions)
        self.questions = random.sample(self.all_questions, sample_size) if len(self.all_questions) <= 1000 else \
            [self.all_questions[i] for i in random.sample(range(len(self.all_questions)), sample_size)]
        self._show_question()

    def _show_question(self):
        if self.question_count >= len(self.questions):
            self._end_quiz()
            return

        # Clear previous widgets
        for widget in [self.question_label, self.count_label, self.remark_label, self.next_btn,
                       self.entry, self.submit_btn] + self.buttons:
            widget.place_forget()

        q = self.questions[self.question_count]
        self.question_label.configure(text=q["question"])
        self.count_label.configure(text=f"QUESTION {self.question_count + 1}/{len(self.questions)}")
        self.remark_label.configure(text=" ")

        # Position labels
        self.question_label.place(relx=0.5, rely=0.25, anchor="c")
        self.count_label.place(relx=0.08, rely=0.1, anchor="c")

        self.answer = self._normalize(q["answer"])

        if "choices" in q:  # Multiple choice
            self.choices = [self._normalize(choice) for choice in q["choices"]]
            self.correct_idx = self.choices.index(self.answer)

            for i, btn in enumerate(self.buttons):
                btn.configure(text=q["choices"][i].upper(), state="normal",
                              fg_color="#3498DB", hover_color="#2980B9")
                btn.place(relx=0.5, rely=0.38 + i * 0.097, anchor="c")
        else:  # Fill in blank
            self.entry.configure(state="normal")
            self.entry.delete(0, "end")
            self.entry = ctk.CTkEntry(self.window, width=600, height=60, font=("Calibri", 20, "bold"), placeholder_text="Enter Text Here")
            self.entry.place(relx=0.4, rely=0.45, anchor="c")
            self.submit_btn.place(relx=0.77, rely=0.45, anchor="c")

    def _check_choice(self, index):
        for btn in self.buttons:
            btn.configure(state="disabled")

        if index == self.correct_idx:
            self.buttons[index].configure(fg_color="green", hover_color="green")
            self.score += 1
            self.remark_label.configure(text="CORRECT!", text_color="green")
        else:
            self.buttons[index].configure(fg_color="red", hover_color="red")
            self.remark_label.configure(text=f"INCORRECT! Answer is {self.answer.upper()}", text_color="yellow")

        self.buttons[self.correct_idx].configure(fg_color="green", hover_color="green")
        self.remark_label.place(relx=0.5, rely=0.8, anchor="c")
        self.next_btn.place(relx=0.5, rely=0.9, anchor="c")

    def _check_entry(self):
        user_answer = self.entry.get()
        if not user_answer:
            CTkMessagebox(title="ENTRY ERROR", message="Entry is Empty. Please Input Your Answer")
            return

        self.entry.configure(state="disabled")
        if self._normalize(user_answer) == self.answer:
            self.score += 1
            self.remark_label.configure(text="CORRECT!", text_color="green")
        else:
            self.remark_label.configure(text=f"INCORRECT! Answer is {self.answer.upper()}", text_color="yellow")

        self.remark_label.place(relx=0.5, rely=0.8, anchor="c")
        self.next_btn.place(relx=0.5, rely=0.9, anchor="c")

    def _next_question(self):
        self.question_count += 1
        self._show_question()

    def _end_quiz(self):
        # Clear all widgets
        for widget in [self.question_label, self.count_label, self.remark_label, self.next_btn,
                       self.entry, self.submit_btn] + self.buttons:
            widget.place_forget()

        percentage = int(self.score / len(self.questions) * 100)
        remark, color = ("Very Good!", "green") if percentage > 90 else \
            ("Good!", "blue") if percentage > 60 else ("Keep Practicing!", "red")

        self.score_label.configure(text=f"{self.score}/{len(self.questions)}")
        self.percent_label.configure(text=f"{percentage}%")
        self.final_remark.configure(text=remark, text_color=color)

        self.score_label.place(relx=0.5, rely=0.35, anchor="c")
        self.percent_label.place(relx=0.5, rely=0.5, anchor="c")
        self.final_remark.place(relx=0.5, rely=0.6, anchor="c")
        self.restart_btn.place(relx=0.5, rely=0.68, anchor="c")

    def _restart(self):
        # Clear end screen widgets
        for widget in [self.score_label, self.percent_label, self.final_remark, self.restart_btn]:
            widget.place_forget()

        self.question_count = 0
        self.score = 0
        self._start_quiz()


if __name__ == "__main__":
    root = ctk.CTk()
    try:
        # You can customize the number of questions here:
        # quiz = Quiz(root, question_bank, 5)    # For 5 questions
        # quiz = Quiz(root, question_bank, 15)   # For 15 questions
        quiz = Quiz(root, question_bank)         # Uses default (10 questions)
        root.mainloop()
    except Exception as e:
        CTkMessagebox(title="APPLICATION ERROR", message=str(e))
        sys.exit()