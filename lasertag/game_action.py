import os
import time
import tkinter as tk
import udp_sockets
import database
from database import clear_table


def create_game_screen(green_team,red_team):
    game_screen = tk.Tk()
    game_screen.title("Game Action Screen")
    width = 1280
    height = 720
    x = (game_screen.winfo_screenwidth()//2)-(width//2)
    y = (game_screen.winfo_screenheight()//2)-(height//2)
    game_screen.geometry('{}x{}+{}+{}'.format(width,height,x,y))
    game_screen.configure(background = 'black')

   # Create frames for each team
    team1_outline = tk.Frame(game_screen, bg="green", bd=2, relief="ridge")
    team1_outline.place(x=10, y=40, width=width//2-20, height= height//2)

    team1_interior = tk.Frame(team1_outline, bg="black")
    team1_interior.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    team2_outline = tk.Frame(game_screen, bg="red", bd=2, relief="ridge")
    team2_outline.place(x=width//2+10, y=40, width=width//2-20, height= height//2)

    team2_interior = tk.Frame(team2_outline, bg="black")
    team2_interior.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    # Add labels for team names
    tk.Label(game_screen, text="Green Team", bg="black", fg="green").place(x=10, y=10)
    tk.Label(game_screen, text="Red Team", bg="black", fg="red").place(x=width//2+10, y=10)

    # Add player names to green team box
    for idx, player_name in enumerate(green_team):
        tk.Label(team1_interior, text=player_name, bg="black", fg="white").grid(row=idx, column=0, padx=5, pady=5)

    # Add player names to red team box
    for idx, player_name in enumerate(red_team):
        tk.Label(team2_interior, text=player_name, bg="black", fg="white").grid(row=idx, column=0, padx=5, pady=5)



    # Create frame for current game action
    current_action_frame = tk.Frame(game_screen, bg="black", bd=2, relief="ridge")
    current_action_frame.place(x=10, y=height//2+50, width=width/2, height=150)

    # Add label for current game action
    tk.Label(current_action_frame, text="Current Game Action", bg="black", fg="blue").pack()

   

    game_screen.mainloop()