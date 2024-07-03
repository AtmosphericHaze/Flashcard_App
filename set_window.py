import tkinter as tk
from tkinter import simpledialog

class SetWindow:
    def __init__(self, root, set_name, flashcards):
        self.root = tk.Toplevel(root)
        self.root.title(set_name)

        self.flashcards = flashcards

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        self.flashcards_listbox = tk.Listbox(self.main_frame, height=10)
        self.flashcards_listbox.pack(side=tk.LEFT, padx=10)
        
        self.update_flashcards_listbox()

        self.add_flashcard_button = tk.Button(self.main_frame, text="Add Flashcard", command=self.add_flashcard)
        self.add_flashcard_button.pack(side=tk.LEFT, padx=10)

    def update_flashcards_listbox(self):
        self.flashcards_listbox.delete(0, tk.END)
        for flashcard in self.flashcards:
            self.flashcards_listbox.insert(tk.END, flashcard['question'])

    def add_flashcard(self):
        question = simpledialog.askstring("Question", "Enter the question:")
        answer = simpledialog.askstring("Answer", "Enter the answer:")
        if question and answer:
            self.flashcards.append({'question': question, 'answer': answer})
            self.update_flashcards_listbox()
