import os
import tkinter as tk
from PIL import Image, ImageTk
import pygame
import random


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width / 2)
    y_coordinate = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x_coordinate, y_coordinate))


def main():
    root = tk.Tk()
    root.title("Countdown")
    root_width = 1280
    root_height = 720
    center_window(root, root_width, root_height)


    # Load and display the first image
    first_image_path = "countdownimages/30.tif"
    first_image = Image.open(first_image_path)
    first_image = first_image.resize((1280, 720))
    first_photo = ImageTk.PhotoImage(first_image)
    image_label = tk.Label(root, image=first_photo)
    image_label.pack(expand=True, fill='both')
    tracks = ["Track01.mp3", "Track02.mp3", "Track03.mp3", "Track04.mp3", "Track06.mp3", "Track07.mp3"]
    random_track = random.choice(tracks)
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
        pygame.mixer.music.load("sounds/{random_track}")
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