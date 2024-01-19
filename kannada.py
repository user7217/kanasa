import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
from gtts import gTTS
import os
import pygame
from google_images_download import google_images_download

# Initialize pygame mixer
pygame.mixer.init()

# Dictionary of Kannada words and their English translations
kannada_words = {
    'ಹಕ್ಕಿ': 'Bird',
    'ಹೂ': 'Flower',
    'ಮನೆ': 'House',
    'ಬಂಗಾಳ': 'Tiger',
    'ನದಿ': 'River',
    'ವನ': 'Forest',
    'ಪ್ರಾಣಿ': 'Animal',
    'ಹಕ್ಕಿಗಳು': 'Birds',
    'ಮೂಡು': 'Three',
    'ಬೆಳಕು': 'Light'
}

# Dictionary of image paths for correct answers
correct_images = {
    'Bird': 'images/Bird_Kannada.jpg',
    'Flower': 'images/Flower_Kannada.jpg',
    'House': 'images/House_Kannada.jpg',
    'Tiger': 'images/Tiger_Kannada.jpg',
    'River': 'images/River_Kannada.jpg',
    'Forest': 'images/Forest_Kannada.jpg',
    'Animal': 'images/Animal_Kannada.jpg',
    'Birds': 'images/Birds_Kannada.jpg',
    'Three': 'images/Three_Kannada.jpg',
    'Light': 'images/Light_Kannada.jpg'
}

class KannadaLearningGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Kannada Learning Game")

        self.score = 0
        self.current_question = None

        # Set up UI elements
        self.style = ttk.Style()

        # Change background color to light yellow
        self.style.configure("TFrame", background="#FFFFE0")

        # Change font color to black
        self.style.configure("TLabel", foreground="black")
        self.style.configure("TButton", foreground="black")

        self.frame = ttk.Frame(master, style="TFrame")
        self.frame.pack(expand=True, fill="both")

        self.label_question = ttk.Label(self.frame, text="", font=("Arial", 14), padding=(0, 10), style="TLabel")
        self.label_question.pack()

        self.options_buttons = []
        for i in range(4):
            button = ttk.Button(self.frame, text="", style="Options.TButton", command=lambda i=i: self.check_answer(i))
            button.pack(pady=5)
            self.options_buttons.append(button)

        self.speak_button = ttk.Button(self.frame, text="Speak", style="Speak.TButton", command=self.speak_word)
        self.speak_button.pack(pady=10)

        self.image_label = ttk.Label(self.frame, image=None, padding=(0, 10))
        self.image_label.pack()

        self.download_images()  # Download images before starting the game
        self.next_question()

    def display_options(self, options):
        for i in range(4):
            self.options_buttons[i].configure(text=options[i])

    def download_images(self):
        response = google_images_download.googleimagesdownload()

        for translation in kannada_words.values():
            arguments = {"keywords": f"{translation} Kannada", "limit": 1, "format": "jpg", "output_directory": "images"}
            try:
                response.download(arguments)
            except Exception as e:
                print(f"Error downloading image for {translation}: {e}")

    def get_image_path(self, translation):
        image_path = f"images/{translation}_Kannada.jpg"
        return image_path if os.path.exists(image_path) else None

    def next_question(self):
        self.current_question = random.choice(list(kannada_words.keys()))
        correct_translation = kannada_words[self.current_question]

        options = random.sample(list(kannada_words.values()), k=3)
        options.append(correct_translation)
        random.shuffle(options)

        self.label_question.configure(text=f"Translate the Kannada word: {self.current_question}")
        self.display_options(options)

        # Remove previous image
        self.image_label.configure(image=None)

    def check_answer(self, user_choice):
        correct_translation = kannada_words[self.current_question]

        if self.options_buttons[user_choice].cget("text") == correct_translation:
            messagebox.showinfo("Correct!", "Good job!")
            self.score += 1

            # Display the image of the correct answer
            image_path = self.get_image_path(correct_translation)
            if image_path:
                image = Image.open(image_path)
                image = ImageTk.PhotoImage(image)
                self.image_label.configure(image=image)
                self.image_label.image = image  # Keep a reference to the image to prevent it from being garbage collected

        else:
            messagebox.showinfo("Incorrect", f"Wrong! The correct translation is: {correct_translation}")

        self.next_question()

    def speak_word(self):
        tts = gTTS(text=self.current_question, lang='kn')
        tts.save("pronunciation.mp3")
        pygame.mixer.music.load("pronunciation.mp3")
        pygame.mixer.music.play()

if __name__ == "__main__":
    root = tk.Tk()

    # Configure style for themed widgets
    style = ttk.Style()
    style.configure("Options.TButton", font=("Arial", 12), padding=(10, 5), background="#FFFFE0", foreground="black")
    style.configure("Speak.TButton", font=("Arial", 12), padding=(10, 5), background="#3498db", foreground="white")

    game = KannadaLearningGame(root)
    root.mainloop()
