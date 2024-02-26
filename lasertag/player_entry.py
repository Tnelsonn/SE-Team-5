import os
import time
import tkinter as tk
import udp_sockets

def submit():
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
    print(all_teams_contents)
    #udp_sockets.game_start()

p_entry = tk.Tk()
p_entry.title("Player Entry")
width = 1280
height = 720
x = (p_entry.winfo_screenwidth()//2)-(width//2)
y = (p_entry.winfo_screenheight()//2)-(height//2)
p_entry.geometry('{}x{}+{}+{}'.format(width,height,x,y))
p_entry.configure(background = 'black')
# Create frames for each team with green and red backgrounds
tf1 = tk.Frame(p_entry, bg="green", padx=5, pady=5)
tf1.grid(row=0, column=0, padx=140, pady=5)
tf2 = tk.Frame(p_entry, bg="red", padx=5, pady=5)
tf2.grid(row=0, column=1, padx=30, pady=5)

# Create lists to hold all Entry widgets for both teams
list_team1 = []
list_team2 = []

# Create labels for column headers
for i, team_frame in enumerate([tf1, tf2]):
    tk.Label(team_frame, text=f"Team {i+1}", font=("Arial", 14, "bold")).grid(row=0, columnspan=3, pady=5)
    for j, col in enumerate(["Id", "Name", "Code Name"]):
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

# Create a Submit button
submit_button = tk.Button(p_entry, text="Submit", command=submit)
submit_button.place(x = 585, y = 670, width = 100)

p_entry.mainloop()
