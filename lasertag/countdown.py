import os
import tkinter as tk
from PIL import Image, ImageTk
import pygame


def main():
    root = tk.Tk()
    root.title("Countdown")
    root.geometry("1280x720")  

    # Load and display the first image
    first_image_path = "countdownimages/30.tif"
    first_image = Image.open(first_image_path)
    first_image = first_image.resize((1280, 720))
    first_photo = ImageTk.PhotoImage(first_image)
    image_label = tk.Label(root, image=first_photo)
    image_label.pack(expand=True, fill='both') 

    # Display Next images
    def show_next_image(index):
        if index < 0:
            root.destroy()
            return
        image_path = f"countdownimages/{index}.tif"
        image = Image.open(image_path)
        image = image.resize((1280, 720))
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo
        root.after(1000, show_next_image, index - 1)

    def start_music():
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/Track07.mp3")
        pygame.mixer.music.play()

    # Start countdown 
    show_next_image(30)

    # Bind the spacebar key to skip countdown 
    def skip_countdown(event):
        root.destroy()
    root.bind("<space>", skip_countdown)


    root.after(16000, start_music)

    root.mainloop()

if __name__ == "__main__":
    main()
