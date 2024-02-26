from supabase import create_client

url = "https://guhvlazcvazrraehvymx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd1aHZsYXpjdmF6cnJhZWh2eW14Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNzI2NDExMiwiZXhwIjoyMDIyODQwMTEyfQ.s9ATaSWw1M5xszV-TBXW0H8wjf-xg089FGf90YKbwws"

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
def insert_player(id, cn):
    if player_exists(id):
        update_player(id, cn)
    else:
        supabase.table("player").insert({"id": id, "codename": cn}).execute()
        

#updates a player
def update_player(id, cn):
    if player_exists(id):
        supabase.table("player").update({"codename": cn}).eq("id", id).execute()
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
#     insert_player(id, "plswork")
#     print(read_table())
#     print('\n\n')

# update_player(2, "update")
# print(read_table())
# print('\n\n')

# insert_player(3, "plswork")
# print(read_table())
# print('\n\n')

# update_player(3, "update")
# print(read_table())
# print('\n\n')

# delete_player(3)
# print(read_table())
    
# clear_table()
# print(read_table())

