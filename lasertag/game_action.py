import os
import time
import tkinter as tk
import database
from database import clear_table
import scoreboard
import socket
import threading

sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address_send = ('localhost', 7500)

update_count = 0


def game_end(socket, address):
    for _ in range(3):
        socket.sendto(b'221', address)
        print('Game end')


def create_game_screen(green_team,red_team,hid):
    game_screen = tk.Tk()
    game_screen.after(360000,game_end,sock_send, server_address_send)
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
    
        
    # Create labels for green and red team scores
    green_label = tk.Label(game_screen, text="Green Team - SCORE: 0", bg="black", fg="green")
    green_label.place(x=10, y=10)

    red_label = tk.Label(game_screen, text="Red Team - SCORE: 0", bg="black", fg="red")
    red_label.place(x=width//2+10, y=10)

    def update_scores():
        # Update the text of the green and red labels with the current scores
        green_label.config(text=f"Green Team - SCORE: {scoreboard.green_score}")
        red_label.config(text=f"Red Team - SCORE: {scoreboard.red_score}")
        
        # Schedule the function to run again after a certain delay
        game_screen.after(10, update_scores)

    # Start updating the scores
    update_scores()
    

    # Add player names to green team box
    for idx, player_name in enumerate(green_team):

        tk.Label(team1_interior, text=player_name, bg="black", fg="white").grid(row=idx, column=0, padx=5, pady=5)

    # Add player names to red team box
    for idx, player_name in enumerate(red_team):
        tk.Label(team2_interior, text=player_name, bg="black", fg="white").grid(row=idx, column=0, padx=5, pady=5)
    


    # Create frame for current game action
    current_action_frame = tk.Frame(game_screen, bg="black", bd=2, relief="ridge")
    current_action_frame.place(x=240, y=height//2+50, width=800, height=250)

    # Add label for current game action
    # Add label for current game action
    tk.Label(current_action_frame, text="Current Game Action", bg="black", fg="blue").pack()
    
    # Create placeholders for values 
    action_labels = []
    
    # Create 10 labels and append them to the list
    for i in range(10):
        label = tk.Label(current_action_frame, text="", bg="black", fg="blue")
        label.pack()
        action_labels.append(label)

    max_updates = 10  # Define the maximum number of updates
    label_texts = [""] * len(action_labels)  # Store the text of each label

    
    # Define function to update action
    def update_action():
        global update_count
        while True:
            current_length = len(scoreboard.player_hits)
            start_index = max(current_length - 10, 0)  # Start index for the last 10 entries
            
            # Update the labels with the last 10 entries of scoreboard.player_hits
            for i in range(min(10, current_length)):
                sender, hit, points = scoreboard.player_hits[start_index + i]
            
                # Find the sender's name corresponding to the ID
                sender_name = next((name for name, id in hid if int(id) == int(sender)), "Unknown")
            
                # Find the hit player's name corresponding to the ID
                hit_name = next((name for name, id in hid if int(id) == int(hit)), "Unknown")
                text = f"{sender_name} hit {hit_name}: {points} points"
                action_labels[i].config(text = text)
            # Make the remaining labels blank
            for i in range(min(10, current_length), 10):
                action_labels[i].config(text="")
            
            # Sleep for a short interval before checking for updates again
            time.sleep(0.5)
    

    update_thread = threading.Thread(target=update_action)
    update_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits
    update_thread.start()
    game_screen.mainloop()