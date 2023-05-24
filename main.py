import tkinter as tk
from tkinter import messagebox
import pymysql

# Connect to the MySQL database
db = pymysql.connect(
    host="rasc.mysql.database.azure.com",
    user="innocode_rasc",
    password="Rasc_062301",
    database="unm_db"
)
cursor = db.cursor()

items = []  # List to store the items
ids = []  # List to store the associated id_unm values

# Create the splash screen window
splash_screen = tk.Tk()
splash_screen.title("Splash Screen")
splash_screen.configure(bg="#B0E2FF")

# Set the splash screen size
splash_width = 300
splash_height = 200
screen_width = splash_screen.winfo_screenwidth()
screen_height = splash_screen.winfo_screenheight()
x = (screen_width - splash_width) // 2
y = (screen_height - splash_height) // 2
splash_screen.geometry(f"{splash_width}x{splash_height}+{x}+{y}")

# Create a canvas for the progress bar
canvas_width = 200
canvas_height = 20
progress_canvas = tk.Canvas(splash_screen, width=canvas_width, height=canvas_height, bg="#E6FFFD", bd=0, highlightthickness=0)
progress_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Draw an empty progress bar rectangle
empty_bar_width = 200
empty_bar_height = 10
empty_bar_x = (canvas_width - empty_bar_width) // 2
empty_bar_y = (canvas_height - empty_bar_height) // 2
empty_bar = progress_canvas.create_rectangle(empty_bar_x, empty_bar_y, empty_bar_x + empty_bar_width, empty_bar_y + empty_bar_height, fill="#FFFFFF", outline="")

# Update the splash screen
splash_screen.update()

# Simulate loading progress
progress_steps = 30
fill_width = 0
fill_height = 10
fill_color = "#90EE90"  # Green color for progress
fill_increment = empty_bar_width / progress_steps
progress_duration = 3  # Duration in seconds

def update_progress(step):
    global fill_width

    if step <= progress_steps:
        fill_width += fill_increment
        fill_bar = progress_canvas.create_rectangle(empty_bar_x, empty_bar_y, empty_bar_x + fill_width, empty_bar_y + fill_height, fill=fill_color, outline="")
        progress_canvas.update()

        # Schedule the next progress update
        splash_screen.after(int(progress_duration * 1000 / progress_steps), update_progress, step + 1)
    else:
        # Destroy the splash screen after the specified duration
        splash_screen.after(int(progress_duration * 1000), splash_screen.destroy)

update_progress(1)

# Start the Tkinter event loop
splash_screen.mainloop()

def populate_listbox():
    # Fetch the items from the database
    cursor.execute("SELECT id_unm, unm_utos FROM unm_list")
    rows = cursor.fetchall()

    # Clear the lists
    items.clear()
    ids.clear()

    # Populate the lists with the fetched items and ids
    for row in rows:
        id_unm, unm_utos = row
        items.append(unm_utos)
        ids.append(id_unm)

    # Clear the listbox
    listbox.delete(0, tk.END)

    # Populate the listbox with the fetched items
    for item in items:
        listbox.insert(tk.END, item)

def add_item():
    item = entry.get()
    if item:
        # Insert the item into the database
        cursor.execute("INSERT INTO unm_list (unm_utos) VALUES (%s)", (item,))
        db.commit()

        # Fetch the last inserted id
        id_unm = cursor.lastrowid

        # Update the lists with the new item and id
        items.append(item)
        ids.append(id_unm)

        # Update the listbox with the new item
        listbox.insert(tk.END, item)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Empty Entry", "Please enter an item.")

def update_item():
    selected_indices = listbox.curselection()
    if selected_indices:
        selected_index = selected_indices[0]  # Get the first selected index
        item = entry.get()
        if item:
            # Get the id_unm value from the selected item
            id_unm = ids[selected_index]

            # Update the item in the database
            cursor.execute("UPDATE unm_list SET unm_utos = %s WHERE id_unm = %s", (item, id_unm))
            db.commit()

            # Update the lists with the new item
            items[selected_index] = item

            # Update the listbox with the new item
            listbox.delete(selected_index)
            listbox.insert(selected_index, item)
            entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Empty Entry", "Please enter an item.")
    else:
        messagebox.showwarning("No Selection", "Please select an item to update.")

def remove_item():
    selected_indices = listbox.curselection()
    if selected_indices:
        selected_index = selected_indices[0]  # Get the first selected index

        # Get the id_unm value from the selected item
        id_unm = ids[selected_index]

        # Delete the item from the database
        cursor.execute("DELETE FROM unm_list WHERE id_unm = %s", (id_unm,))
        db.commit()

        # Delete the item from the lists
        items.pop(selected_index)
        ids.pop(selected_index)

        # Delete the item from the listbox
        listbox.delete(selected_index)
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("No Selection", "Please select an item to remove.")

# Create the main window
window = tk.Tk()
window.title("Utos ni Mama ListApp")

# Set the background color to light blue
window.configure(bg="#B0E2FF")

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window size and position it in the center
window_width = 400
window_height = 500
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create the listbox to display the items
listbox = tk.Listbox(window, bg="#E6FFFD")
listbox.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

# Create an entry field to add/update items
entry = tk.Entry(window, bg="#E6FFFD")
entry.pack(padx=10, pady=5, fill=tk.BOTH)

# Create a frame to hold the buttons
button_frame = tk.Frame(window)
button_frame.pack(padx=10, pady=5)

# Define the font size
button_font = ("Arial", 12)

# Determine the button width based on the longest button text
button_texts = ["Add", "Update", "Remove"]
button_width = max(len(text) for text in button_texts) + 2

# Create buttons for adding, updating, and removing items
add_button = tk.Button(button_frame, text="Add", command=add_item, bg="#90EE90", fg="black", font=button_font, width=button_width)
add_button.pack(side=tk.LEFT, padx=2)

update_button = tk.Button(button_frame, text="Update", command=update_item, bg="#FFD700", fg="black", font=button_font, width=button_width)
update_button.pack(side=tk.LEFT, padx=2)

remove_button = tk.Button(button_frame, text="Remove", command=remove_item, bg="#FF6347", fg="black", font=button_font, width=button_width)
remove_button.pack(side=tk.LEFT, padx=2)

# Populate the listbox with the items from the database
populate_listbox()

# Start the tkinter event loop
window.mainloop()
