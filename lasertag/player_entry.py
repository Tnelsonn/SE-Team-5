import os
import time
import tkinter as tk
from PIL import Image, ImageTk
import udp_sockets
import database
from database import clear_table
from game_action import create_game_screen
from countdown import main

#get socket information
sock_send, sock_receive, server_address_send, server_address_receive = udp_sockets.create_sockets()

green_team = []
red_team = []

def submit():

    global green_team, red_team  # Declare global lists to store player names
    
    # Clear the existing player lists
    green_team.clear()
    red_team.clear()

    all_teams_contents = []
    for team_entry_list in [list_team1, list_team2]:
        team_contents = []
        for i in range(20):
            row = []
            for j in range(3):
                cell_value = team_entry_list[i][j].get()
                row.append(cell_value)
            team_contents.append(row)
        all_teams_contents.append(team_contents)
        
    for team_contents, team_name in zip(all_teams_contents, ['Team 1', 'Team 2']):
        for player_info in team_contents:
            player_id, player_codename, player_hid = player_info
            if player_id.strip() and player_codename.strip():
                if int(player_id.strip())%2 == 1:
                    green_team.append(player_codename.strip())
                else:
                    red_team.append(player_codename.strip())
                database.insert_player(player_id, player_codename,player_hid)
                udp_sockets.transmit_data(sock_send, server_address_send, player_id)
        
#clear entries and database       
def clear_entries(event=None):
    for entry_list in [list_team1, list_team2]:
        for entry_row in entry_list:
            for entry in entry_row:
                entry.delete(0, tk.END)
    clear_table()



p_entry = tk.Tk()
p_entry.title("Player Entry")
width = 1280
height = 720
x = (p_entry.winfo_screenwidth()//2)-(width//2)
y = (p_entry.winfo_screenheight()//2)-(height//2)
p_entry.geometry('{}x{}+{}+{}'.format(width,height,x,y))
p_entry.configure(background = 'black')
# Create frames for each team with green and red backgrounds

container_frame = tk.Frame(p_entry, bg="black")
container_frame.pack(expand=True, fill="both")


tf1 = tk.Frame(container_frame, bg="green", padx=5, pady=5)
tf1.pack(side=tk.LEFT, padx=50, pady=5)
tf2 = tk.Frame(container_frame, bg="red", padx=5, pady=5)
tf2.pack(side=tk.LEFT, padx=50, pady=5)

container_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
# Create lists to hold all Entry widgets for both teams
list_team1 = []
list_team2 = []

# Create labels for column headers
for i, team_frame in enumerate([tf1, tf2]):
    tk.Label(team_frame, text=f"Team {i+1}", font=("Arial", 14, "bold")).grid(row=0, columnspan=2, pady=5)
    for j, col in enumerate(["Id", "Code Name", "Hardware ID"]):
        tk.Label(team_frame, text=col, font=("Arial", 10, "bold"),width = 10).grid(row=1, column=j, pady=5)

# Create the tables of Entry widgets for both teams
for team_entry_list, team_frame in [(list_team1, tf1), (list_team2, tf2)]:
    for i in range(20):
        row_entries = []
        for j in range(3):
            entry = tk.Entry(team_frame)
            entry.grid(row=i+2, column=j, padx=5, pady=5)
            row_entries.append(entry)
        team_entry_list.append(row_entries)



def switch_to_game_screen(event=None):
    p_entry.destroy()
    if __name__ == "__main__":
        main()
    create_game_screen(green_team, red_team)

# create a button to start the game
clear_button = tk.Button(p_entry, text="Start Game\nF5", command=switch_to_game_screen)
clear_button.pack(side = tk.BOTTOM , anchor = tk.CENTER, padx = 10, pady = 30)
p_entry.bind("<F5>", switch_to_game_screen)

#create a clear entries button
clear_button = tk.Button(p_entry, text="Clear\nF12", command=clear_entries)
clear_button.pack(side = tk.BOTTOM , anchor = tk.CENTER, padx = 10, pady = 0)
p_entry.bind("<F12>", clear_entries)

# Create a Submit button
submit_button = tk.Button(p_entry, text="Submit", command=submit)
submit_button.pack(side = tk.BOTTOM , anchor = tk.CENTER, padx = 10, pady = 30)

p_entry.mainloop()