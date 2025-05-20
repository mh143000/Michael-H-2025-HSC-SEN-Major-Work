#FORM INPUT WINDOWED APP... uses tkinter windowed message boxes (see YR11 SEN tutorials)
#PROTOTYPE MODULE... next task figure out how to use a HTML form for this purpose
import sqlite3
    
conn = sqlite3.connect('mydatabase.db') #create db temp name
cursor = conn.cursor() #db
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mytable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        city TEXT
    )
''')
conn.commit()
conn.close()

#message box functionality
import tkinter as tk
import sqlite3
from tkinter import messagebox

#def. functions for the data collected from form window
def submit_data():
    name = name_entry.get()
    age = age_entry.get()
    city = city_entry.get()

#error mitigation prevent empty/shallow inputs
    if not name or not age or not city:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    try:
        age = int(age) #ensures age is integer as defined in sql database connection and here
    except ValueError:
            messagebox.showerror("Error", "Age must be a number")
            return

    conn = sqlite3.connect('mydatabase.db') #input form data into respective places in db
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mytable (name, age, city) VALUES (?, ?, ?)", (name, age, city))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Data submitted successfully.")
    clear_fields()

#clear_fields function clears all form input box fields to allow for new entry
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)

#creating the windowed form box:
window = tk.Tk()
window.title("Data Entry Form")

tk.Label(window, text="Name:").grid(row=0, column=0) #name label next to input field
name_entry = tk.Entry(window)
name_entry.grid(row=0, column=1) #entry field

tk.Label(window, text="Age:").grid(row=1, column=0) #age ditto
age_entry = tk.Entry(window)
age_entry.grid(row=1, column=1)

tk.Label(window, text="City:").grid(row=2, column=0) #city ditto
city_entry = tk.Entry(window)
city_entry.grid(row=2, column=1)

submit_button = tk.Button(window, text="Submit", command=submit_data) #create submit button
submit_button.grid(row=3, column=1)

clear_button = tk.Button(window, text="Clear", command=clear_fields) #ditto clear
clear_button.grid(row=3, column=0)

#loops functionality of window to allow for more entries
window.mainloop()
