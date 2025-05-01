import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from random import shuffle
import os
import time

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz By Shoaib")
        self.root.geometry("600x500")
        
        # Variables
        self.selected_difficulty = tk.StringVar()
        self.current_question = 0
        self.score = 0
        self.selected_option = tk.StringVar(value="")  # Initialize as empty
        self.time_left = 15
        self.timer_id = None
        
        # Create frames
        self.main_frame = tk.Frame(self.root)
        self.quiz_frame = tk.Frame(self.root)
        self.result_frame = tk.Frame(self.root)
        
        # Try to load questions automatically
        self.questions = {'easy': [], 'medium': [], 'hard': []}
        if not self.load_questions():
            self.show_file_selection()
        else:
            self.show_main_screen()
    
    def show_file_selection(self):
        self.clear_frames()
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(self.main_frame, text="Quiz By Shoaib", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Label(self.main_frame, text="Could not find quiz questions file", font=("Arial", 14)).pack(pady=10)
        
        tk.Button(
            self.main_frame, 
            text="Select Quiz Questions CSV File", 
            command=self.select_csv_file,
            font=("Arial", 14),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=20)
    
    def select_csv_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Quiz Questions CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )
        if file_path:
            if self.load_questions(file_path):
                self.show_main_screen()
            else:
                messagebox.showerror("Error", "Could not load questions from the selected file")
    
    def load_questions(self, file_path=None):
        try:
            if not file_path:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(script_dir, 'quiz_questions.csv')
                if not os.path.exists(file_path):
                    return False
            
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                self.questions = {'easy': [], 'medium': [], 'hard': []}
                for row in reader:
                    self.questions[row['difficulty']].append({
                        'question': row['question'],
                        'options': [row['option1'], row['option2'], row['option3'], row['option4']],
                        'answer': row['answer']
                    })
                
                for difficulty in self.questions:
                    shuffle(self.questions[difficulty])
                
                return True
        except Exception as e:
            print(f"Error loading questions: {e}")
            return False
    
    def show_main_screen(self):
        self.clear_frames()
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(self.main_frame, text="Quiz By Shoaib", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Label(self.main_frame, text="Select Difficulty Level:", font=("Arial", 16)).pack(pady=10)
        
        difficulties = [('Easy', 'easy'), ('Medium', 'medium'), ('Hard', 'hard')]
        for text, difficulty in difficulties:
            tk.Radiobutton(
                self.main_frame, 
                text=text, 
                variable=self.selected_difficulty, 
                value=difficulty,
                font=("Arial", 14)
            ).pack(pady=5, anchor="w")
        
        tk.Button(
            self.main_frame, 
            text="Start Quiz", 
            command=self.start_quiz,
            font=("Arial", 14),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=20)
    
    def start_quiz(self):
        difficulty = self.selected_difficulty.get()
        if not difficulty:
            return
        
        self.quiz_questions = self.questions[difficulty][:10]
        self.current_question = 0
        self.score = 0
        self.show_question()
    
    def start_timer(self):
        self.time_left = 15
        if hasattr(self, 'timer_id') and self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.update_timer()
    
    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time's up!", fg="red")
            self.next_question()
    
    def show_question(self):
        self.clear_frames()
        self.quiz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Timer
        self.timer_label = tk.Label(
            self.quiz_frame, 
            text="Time left: 15s", 
            font=("Arial", 12, "bold"),
            fg="blue"
        )
        self.timer_label.pack(anchor="ne")
        self.start_timer()
        
        # Progress bar
        progress_value = (self.current_question + 1) / len(self.quiz_questions) * 100
        progress = ttk.Progressbar(
            self.quiz_frame, 
            orient="horizontal", 
            length=500, 
            mode="determinate", 
            value=progress_value
        )
        progress.pack(fill=tk.X, pady=10)
        
        # Question
        question_data = self.quiz_questions[self.current_question]
        question_text = f"Question {self.current_question + 1}/{len(self.quiz_questions)}: {question_data['question']}"
        tk.Label(
            self.quiz_frame, 
            text=question_text, 
            font=("Arial", 12),
            wraplength=550,
            justify="left"
        ).pack(pady=10, anchor="w")
        
        # Options
        options_frame = tk.Frame(self.quiz_frame)
        options_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Reset selection for new question
        self.selected_option.set("")
        
        for option in question_data['options']:
            rb = tk.Radiobutton(
                options_frame, 
                text=option, 
                variable=self.selected_option, 
                value=option,
                font=("Arial", 11),
                wraplength=500,
                justify="left",
                indicatoron=1,
                selectcolor="white"
            )
            rb.pack(anchor="w", padx=20, pady=5)
            rb.bind("<Button-1>", lambda e: self.option_selected())
        
        # Navigation buttons (initially hidden)
        self.button_frame = tk.Frame(self.quiz_frame)
        self.button_frame.pack(pady=10)
        
        if self.current_question < len(self.quiz_questions) - 1:
            self.next_button = tk.Button(
                self.button_frame, 
                text="Next", 
                command=self.next_question,
                font=("Arial", 12),
                bg="#2196F3",
                fg="white"
            )
        else:
            self.submit_button = tk.Button(
                self.button_frame, 
                text="Submit Quiz", 
                command=self.show_results,
                font=("Arial", 12),
                bg="#4CAF50",
                fg="white"
            )
    
    def option_selected(self):
        if self.current_question < len(self.quiz_questions) - 1:
            self.next_button.pack(side=tk.RIGHT, padx=10)
        else:
            self.submit_button.pack(side=tk.RIGHT, padx=10)
    
    def next_question(self):
        if hasattr(self, 'timer_id') and self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.check_answer()
        self.current_question += 1
        self.show_question()
    
    def check_answer(self):
        question_data = self.quiz_questions[self.current_question]
        if self.selected_option.get() == question_data['answer']:
            self.score += 1
    
    def show_results(self):
        if hasattr(self, 'timer_id') and self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.check_answer()
        self.clear_frames()
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Score display
        score_text = f"Your Score: {self.score}/{len(self.quiz_questions)}"
        tk.Label(
            self.result_frame, 
            text=score_text, 
            font=("Arial", 24, "bold")
        ).pack(pady=20)
        
        # Percentage
        percentage = (self.score / len(self.quiz_questions)) * 100
        tk.Label(
            self.result_frame, 
            text=f"{percentage:.1f}% Correct", 
            font=("Arial", 18)
        ).pack(pady=10)
        
        # Restart button
        tk.Button(
            self.result_frame, 
            text="Restart Quiz", 
            command=self.show_main_screen,
            font=("Arial", 14),
            bg="#FF9800",
            fg="white"
        ).pack(pady=20)
    
    def clear_frames(self):
        for frame in [self.main_frame, self.quiz_frame, self.result_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
            frame.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()