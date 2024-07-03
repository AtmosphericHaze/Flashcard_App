import tkinter as tk
from tkinter import simpledialog, messagebox

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")

        # Lista zestawów
        self.sets = {}

        # Główna ramka
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Wywołaj metodę, aby wyświetlić zestawy fiszek
        self.show_sets()

    def show_sets(self):
        # Wyczyszczenie ramki
        self.clear_frame()

        # Wyświetlanie listy zestawów
        self.sets_listbox = tk.Listbox(self.main_frame, height=10)
        self.sets_listbox.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.sets_listbox.bind('<Double-1>', self.open_set)
        
        self.add_set_button = tk.Button(self.main_frame, text="Add Set", command=self.add_set)
        self.add_set_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.update_sets_listbox()

    def add_set(self):
        set_name = simpledialog.askstring("Set Name", "Enter the name of the new set:")
        if set_name:
            self.sets[set_name] = []
            self.update_sets_listbox()

    def update_sets_listbox(self):
        self.sets_listbox.delete(0, tk.END)
        for set_name in self.sets:
            self.sets_listbox.insert(tk.END, set_name)

    def open_set(self, event):
        selected_set = self.sets_listbox.get(self.sets_listbox.curselection())
        self.show_flashcards(selected_set)

    def show_flashcards(self, set_name):
        # Wyczyszczenie ramki
        self.clear_frame()

        self.flashcards = self.sets[set_name]

        self.flashcards_listbox = tk.Listbox(self.main_frame, height=10)
        self.flashcards_listbox.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.update_flashcards_listbox()

        self.add_flashcard_button = tk.Button(self.main_frame, text="Add Flashcard", command=self.add_flashcard)
        self.add_flashcard_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.back_button = tk.Button(self.main_frame, text="Back to Sets", command=self.show_sets)
        self.back_button.pack(side=tk.LEFT, padx=10, pady=10)

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

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
