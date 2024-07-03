import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from PIL import Image, ImageTk
import os
from file_operations import save_all_sets, load_sets

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")

        # Lista zestawów
        self.sets = {}

        # Ścieżka do folderu zapisu
        self.save_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'My Flashcards')
        os.makedirs(self.save_folder, exist_ok=True)

        # Główna ramka
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Menu
        self.create_menu()

        # Wczytaj istniejące zestawy fiszek
        self.sets = load_sets(self.save_folder)
        
        # Wywołaj metodę, aby wyświetlić zestawy fiszek
        self.show_sets()

        # Obsługa zamknięcia aplikacji
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_sets_to_file)
        file_menu.add_command(label="Load", command=self.load_sets_from_file)

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

        self.add_flashcard_button = tk.Button(self.main_frame, text="Add Flashcard", command=lambda: self.open_add_flashcard_dialog(set_name))
        self.add_flashcard_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.back_button = tk.Button(self.main_frame, text="Back to Sets", command=self.show_sets)
        self.back_button.pack(side=tk.LEFT, padx=10, pady=10)

    def update_flashcards_listbox(self):
        self.flashcards_listbox.delete(0, tk.END)
        for flashcard in self.flashcards:
            display_text = flashcard['title']
            if 'image' in flashcard and flashcard['image']:
                display_text += " (Image)"
            self.flashcards_listbox.insert(tk.END, display_text)

    def open_add_flashcard_dialog(self, set_name):
        AddFlashcardDialog(self.root, set_name, self.sets[set_name], self.update_flashcards_listbox)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def save_sets_to_file(self):
        save_all_sets(self.sets, self.save_folder)
        messagebox.showinfo("Save", f"Sets saved successfully to {self.save_folder}.")

    def load_sets_from_file(self):
        self.sets = load_sets(self.save_folder)
        self.update_sets_listbox()
        messagebox.showinfo("Load", f"Sets loaded successfully from {self.save_folder}.")

    def on_closing(self):
        self.save_sets_to_file()
        self.root.destroy()

class AddFlashcardDialog:
    def __init__(self, root, set_name, flashcards, update_callback):
        self.flashcards = flashcards
        self.update_callback = update_callback
        self.image_path = None

        self.dialog = tk.Toplevel(root)
        self.dialog.title(f"Add Flashcard to {set_name}")

        tk.Label(self.dialog, text="Title:").pack(pady=5)
        self.title_entry = tk.Entry(self.dialog, width=50)
        self.title_entry.pack(pady=5)

        tk.Label(self.dialog, text="Description:").pack(pady=5)
        self.description_entry = tk.Entry(self.dialog, width=50)
        self.description_entry.pack(pady=5)

        self.add_image_button = tk.Button(self.dialog, text="Add Image", command=self.add_image)
        self.add_image_button.pack(pady=5)

        self.add_flashcard_button = tk.Button(self.dialog, text="Add Flashcard", command=self.add_flashcard)
        self.add_flashcard_button.pack(pady=5)

    def add_image(self):
        self.image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if self.image_path:
            self.add_image_button.config(text="Image Added")

    def add_flashcard(self):
        title = self.title_entry.get()
        description = self.description_entry.get()

        if title and description:
            new_flashcard = {'title': title, 'description': description, 'image': self.image_path}
            self.flashcards.append(new_flashcard)
            self.update_callback()
            self.dialog.destroy()
        else:
            messagebox.showwarning("Input Error", "Please fill in both the title and description.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
