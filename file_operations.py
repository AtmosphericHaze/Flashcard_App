import json
import os
import shutil

def save_set(set_name, flashcards, save_folder):
    # Tworzenie folderu na zestaw, jeśli nie istnieje
    set_folder = os.path.join(save_folder, set_name)
    os.makedirs(set_folder, exist_ok=True)

    # Kopiowanie obrazów do dedykowanego folderu i aktualizacja ścieżek
    for flashcard in flashcards:
        if flashcard['image']:
            image_path = flashcard['image']
            if os.path.isfile(image_path):
                new_image_path = os.path.join(set_folder, os.path.basename(image_path))
                shutil.copy(image_path, new_image_path)
                flashcard['image'] = os.path.relpath(new_image_path, save_folder)

    # Zapis fiszek do pliku JSON
    set_file = os.path.join(set_folder, 'flashcards.json')
    with open(set_file, 'w') as file:
        json.dump(flashcards, file, indent=4)

def load_sets(save_folder):
    sets = {}
    if os.path.isdir(save_folder):
        for set_name in os.listdir(save_folder):
            set_folder = os.path.join(save_folder, set_name)
            if os.path.isdir(set_folder):
                set_file = os.path.join(set_folder, 'flashcards.json')
                try:
                    with open(set_file, 'r') as file:
                        sets[set_name] = json.load(file)
                except FileNotFoundError:
                    sets[set_name] = []
    return sets

def save_all_sets(sets, save_folder):
    for set_name, flashcards in sets.items():
        save_set(set_name, flashcards, save_folder)
