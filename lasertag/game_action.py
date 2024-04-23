import os
import subprocess
import time
import tkinter as tk
import database
from database import clear_table
import scoreboard
import socket
import threading
import udp_sockets

sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address_send = ('localhost', 7500)

update_count = 0




def game_end(socket, address):
    for _ in range(3):
        socket.sendto(b'221', address)
        print('Game end')


def create_game_screen(green_team,red_team,hid,player_hid_data):
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
    green_label = tk.Label(game_screen, text="Green Team - SCORE: 0", bg="black", fg="white",font='Helvetica 18 bold')
    green_label.place(x=10, y=10)

    red_label = tk.Label(game_screen, text="Red Team - SCORE: 0", bg="black", fg="white",font='Helvetica 18 bold')
    red_label.place(x=width//2+10, y=10)

    def flash_team_labels():
        def flash(label):
            # Define colors to alternate between
            colors = ["black", "white"]
            # Alternate between colors
            for color in colors:
                label.config(fg=color)
                game_screen.update()
                game_screen.after(500)  

        # Get the current scores
        green_score = scoreboard.green_score
        red_score = scoreboard.red_score

        # Determine which team has a higher score
        if green_score > red_score:
            flash(green_label)  # Flash the green team label
        elif red_score > green_score:
            flash(red_label)    # Flash the red team label
        else:
            # In case of a tie, flash both labels
            flash(green_label)
            flash(red_label)


    def flash_label(label):
        def flash():
            # Define colors to alternate between
            colors = ["black", "white"]

            # Alternate between colors
            for color in colors:
                label.config(fg=color)
                game_screen.update()  # Update the display
                game_screen.after(500)  # Wait for 500 milliseconds before changing color

        # Start flashing
        flash()
    
    def flash_highest_scorer(green_scores, red_scores):
        # Combine green and red scores
        all_scores = green_scores + red_scores

        # Find the player with the highest score
        highest_scorer = max(all_scores, key=lambda x: x[1])

        # Determine the team of the highest scorer
        if highest_scorer in green_scores:
            team_labels = green_labels
        else:
            team_labels = red_labels

        # Find the label associated with the highest scorer
        for label in team_labels:
            player_name = label.cget("text").split(" - ")[0]  # Get the player name from the label text
            if player_name == highest_scorer[0]:
                flash_label(label)  # Flash the label of the highest scorer
                break

    def update_player_scores():
        while True:
            # Update label texts for green team players
            green_scores = [(player_name, scoreboard.board.get(player_hid_data.get(player_name, ""), 0)) for player_name in green_team]
            green_scores.sort(key=lambda x: x[1], reverse=True)  # Sort players based on scores
            for idx, (player_name, score) in enumerate(green_scores):
                hid = player_hid_data.get(player_name, "")    
                label_text = f"{player_name} - Score: {score}"
                green_labels[idx].config(text=label_text)
                

            # Update label texts for red team players
            red_scores = [(player_name, scoreboard.board.get(player_hid_data.get(player_name, ""), 0)) for player_name in red_team]
            red_scores.sort(key=lambda x: x[1], reverse=True)  # Sort players based on scores
            for idx, (player_name, score) in enumerate(red_scores):
                hid = player_hid_data.get(player_name, "")    
                label_text = f"{player_name} - Score: {score}"
                red_labels[idx].config(text=label_text)

            flash_highest_scorer(green_scores, red_scores)
            flash_team_labels()
            green_label.config(text=f"Green Team - SCORE: {scoreboard.green_score}")
            red_label.config(text=f"Red Team - SCORE: {scoreboard.red_score}")

            time.sleep(0.5)


    green_labels = []
    for idx, player_name in enumerate(green_team):
        label = tk.Label(team1_interior, text=f"{player_name} - Score: 0", bg="black", fg="white",font='Helvetica 18 bold')
        label.grid(row=idx, column=0, padx=5, pady=5)
        green_labels.append(label)

    # Create labels for each player in the red team
    red_labels = []
    for idx, player_name in enumerate(red_team):
        label = tk.Label(team2_interior, text=f"{player_name} - Score: 0", bg="black", fg="white",font='Helvetica 18 bold')
        label.grid(row=idx, column=1, padx=5, pady=5)
        red_labels.append(label)

    

    # Create frame for current game action
    current_action_frame = tk.Frame(game_screen, bg="black", bd=2, relief="ridge")
    current_action_frame.place(x=240, y=height//2+50, width=800, height=250)

    # Add label for current game action
    # Add label for current game action
    tk.Label(current_action_frame, text="Current Game Action", bg="black", fg="blue",font='Helvetica 18 bold').pack()
    
    # Create placeholders for values 
    action_labels = []
    
    # Create 10 labels and append them to the list
    for i in range(10):
        label = tk.Label(current_action_frame, text="", bg="black", fg="blue",font='Helvetica 18 bold')
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

    def go_back_to_player_entry():
        # Close the socket
        game_screen.destroy()  # Close the current game screen
        udp_sockets.cleanup()
        udp_sockets.stop_receive_thread()
       
            
            # Open the player entry screen
        status = os.system("python3 player_entry.py")
        print(status)
        
       


    # Create a button to go back to the player entry screen
    back_button = tk.Button(game_screen, text="Back to Player Entry", command=go_back_to_player_entry)
    back_button.pack(side = tk.BOTTOM , anchor = tk.CENTER, padx = 10, pady = 30)

    
    update_player_thread = threading.Thread(target=update_player_scores)
    update_player_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits
    update_player_thread.start()
    update_thread = threading.Thread(target=update_action)
    update_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits
    update_thread.start()
    game_screen.mainloop()