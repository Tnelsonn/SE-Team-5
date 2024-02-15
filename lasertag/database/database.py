from dotenv import load_dotenv
load_dotenv()

import os

from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

#instantiates supabase client
supabase = create_client(url, key)

#returns entire data table
def read_table():
    table = supabase.table("player").select("*").execute()
    return table.data #table.data is used to access list of player dictionaries

#checks to see if player id is being used
def player_exists(id):
    existing_player = supabase.table("player").select("id").eq("id", id).execute()
    if existing_player.data: #returns false if there if data is empty
        return True
    else: 
        return False

#insert data player
#requires id #, first name, last name, codename 
def insert_player(id, fn, ln, cn):
    if player_exists(id):
        print("Cannot insert player, id is already being used.\n")
    else:
        supabase.table("player").insert({"id": id, "first_name": fn, "last_name": ln, "codename": cn}).execute()


#updates a player
def update_player(id, fn, ln, cn):
    if player_exists(id):
        supabase.table("player").update({"first_name": fn, "last_name": ln, "codename": cn}).eq("id", id).execute()
    else:  
        print("Cannot update player that does not exist.\n")

#deletes player based on id
def delete_player(id):
    supabase.table("player").delete().eq("id", id).execute()

#clear table
def clear_table():
    #read table
    all_rows = read_table()

    #loop through data
    for rows in all_rows:
        delete_player(rows['id'])


#testing
# clear_table()
# print(read_table())
# print('\n\n')

# for id in range(10):
#     insert_player(id, "Ethan", "Smith", "plswork")
#     print(read_table())
#     print('\n\n')

# update_player(2, "Smith", "Ethan", "update")
# print(read_table())
# print('\n\n')

# insert_player(3, "Ethan", "Smith", "plswork")
# print(read_table())
# print('\n\n')

# update_player(3, "Smith", "Ethan", "update")
# print(read_table())
# print('\n\n')

# delete_player(3)
# print(read_table())
    
# clear_table()
# print(read_table())

