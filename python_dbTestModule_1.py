import sqlite3
#EDIT OF ELECTIVES DATA-BASE TO DRAFT DEMONSTRATE A BASIC TRANSPORT FLEET DATA-BASE
    #step 1: Setup SQL
#---------------------------------------------------------------
    #Connects to the SQL lite DB (or it creates it if it does not exist)
conn = sqlite3.connect('test_asset_fleet.db')
    #Create a cursor object to execute SQL commands 
cursor = conn.cursor()
    #Create a table to store the electives and the relevant fields plus data types of the fields
cursor.execute('''CREATE TABLE IF NOT EXISTS test_asset_fleet(
asset_id INTEGER PRIMARY KEY,
asset_name TEXT,
call_sign TEXT,
vehicle_model TEXT,
rego_number TEXT,
capacity INTEGER)
''')
    #Commit changes and close the connection to the DB
conn.commit()
#---------------------------------------------------------------

    #step 2: Setup functions to read and insert data into/from the DB
def add_asset():
    asset_name = input("Enter asset name (E.g. Long-Bus): ")
    call_sign = input("Enter the asset's unit number: ")
    vehicle_model = input("Enter the vehicle model (E.g. Volvo B7RLE): ")
    rego_number = input("Enter the rego/plate number of the vehicle: ")
    capacity = input("Enter the seating capacity of the vehicle: ")


    #insert our variables data into the DB
    cursor.execute('''
    INSERT INTO test_asset_fleet (asset_name, call_sign, vehicle_model, rego_number, capacity)
    VALUES(?, ?, ?, ?, ?)
    ''', (asset_name, call_sign, vehicle_model, rego_number, capacity))
    conn.commit()
    print("Asset added successfully")
    print("You have entered:", asset_name, vehicle_model, ".. call sign", call_sign, ".. registered", rego_number, ".. with seating capacity of", capacity)

def show_all_assets():
    #Reads all the data from the DB
    cursor.execute("SELECT * FROM test_asset_fleet")
    records = cursor.fetchall()
    for record in records:
        print(record)

def show_all_assets_desc():
    #Reads all the data from the DB in descending order
    cursor.execute ('''SELECT * FROM test_asset_fleet
                    ORDER BY asset_id DESC''')
    records = cursor.fetchall()
    for record in records:
        print(record)
#---------------------------------------------------------------

#step 3: writing a mainline to add and view electives
finished = False
while(finished == False): 
    add_asset()
    no_more = input("Add more assets? Y or N: ")
    if no_more == "N":
        finished = True

#Ask what order to show enrolments
input("What order would you like to see the asset fleet? Ascending in asset_id or descending? Type 'ASC' or 'DESC' ")
if input == "ASC":
    show_all_assets()
else:
    show_all_assets_desc()
#---------------------------------------------------------------
