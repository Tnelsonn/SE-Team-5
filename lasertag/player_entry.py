import os
import time
import tkinter as tk
from PIL import Image, ImageTk
import udp_sockets
import database as db
from game_action import create_game_screen
from countdown import main
import threading

<<<<<<< HEAD
=======


>>>>>>> 2d15881907dbb0a7b301063f40f5aedca37f8745
#create sockets
sock_send, sock_receive, server_address_send, server_address_receive = udp_sockets.create_sockets()
udp_sockets.bind_sockets()

<<<<<<< HEAD
=======
udp_sockets.bind_sockets()

>>>>>>> 2d15881907dbb0a7b301063f40f5aedca37f8745
#create thread for receiving statuses
socket_thread = threading.Thread(target=udp_sockets.receive_data)
socket_thread.start()

#lists of player info for each team
green_team = []
red_team = []

#lists of only codenames for each team
green_team_cn = []
red_team_cn = []
hid = []
player_hid_data = dict()
hid.append(("Red Base",53))
hid.append(("Green Base",43))

def load_db():
    #get all current rows in the db
    players = db.read_table()

    #check to see if db is empty
    if not players:
        return
    
    #sort players by team
    for player in players:
        player_hid =  player.get('hardware_id', '')
        player_codename = player.get('codename', '')
        hid.append((player_codename.strip(),int(player_hid.strip())))
        player_hid_data[player_codename.strip()]=int(player_hid.strip())
        if int(player_hid.strip())%2 == 0:
            green_team.append(player)
            green_team_cn.append(player_codename.strip())
            
        else:
            red_team.append(player)
            red_team_cn.append(player_codename.strip())
            
<<<<<<< HEAD
            
=======
          
>>>>>>> 2d15881907dbb0a7b301063f40f5aedca37f8745
def fill_tables():
    #load current db
    load_db()    
    
    #insert green team data
    for i, player_info in enumerate(green_team):
        if i < len(list_team1):
            entry_row = list_team1[i]
            #populate the entry widgets with player information
            for j, entry in enumerate(entry_row):
                entry.delete(0, tk.END)
                if j == 0:
                    value = player_info.get('id', '') 
                elif j == 1:
                    value = player_info.get('codename', '')  
                elif j == 2:
                    value = player_info.get('hardware_id', '') 
                entry.insert(tk.END, value)

    #insert red team data
    for i, player_info in enumerate(red_team):
        if i < len(list_team2):
            entry_row = list_team2[i]
            #populate the entry widgets with player information
            for j, entry in enumerate(entry_row):
                entry.delete(0, tk.END)
                if j == 0:
                    value = player_info.get('id', '')
                elif j == 1:
                    value = player_info.get('codename', '')
                elif j == 2:
                    value = player_info.get('hardware_id', '')
                entry.insert(tk.END, value)

def submit():

    global green_team_cn, red_team_cn  # Declare global lists to store player names
    
    # Clear the existing player lists
    green_team_cn.clear()
    red_team_cn.clear()

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
                if int(player_hid.strip())%2 == 1:
                    green_team_cn.append(player_codename.strip())
                else:
                    red_team_cn.append(player_codename.strip())
                db.insert_player(player_id, player_codename,player_hid) #this function will handle cases where player already exists
                udp_sockets.transmit_data(sock_send, server_address_send, player_id)
        
#clear entries and database       
def clear_entries(event=None):
    for entry_list in [list_team1, list_team2]:
        for entry_row in entry_list:
            for entry in entry_row:
                entry.delete(0, tk.END)
    db.clear_table()

def switch_to_game_screen(event=None):
    p_entry.destroy()
    #os.system("Python3 tg.py")
    if __name__ == "__main__":
        main()
    udp_sockets.game_start(sock_send, server_address_send)
    create_game_screen(green_team_cn, red_team_cn,hid,player_hid_data)
<<<<<<< HEAD
    
=======
>>>>>>> 2d15881907dbb0a7b301063f40f5aedca37f8745
    
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

#populate the widgets with current db
fill_tables()

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