import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Connect to the database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your pw here",
            database="HotelManagementSystem"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None

def view_all_details():
    # Create the second main window
    details_window = Toplevel(root)
    details_window.title("All Room and Guest Information")
    details_window.geometry("1200x800")  # Adjust size as needed

    # Create a notebook for tabs
    notebook = ttk.Notebook(details_window)
    notebook.pack(fill=BOTH, expand=True)

    # Tab for Room Details
    room_tab = Frame(notebook)
    notebook.add(room_tab, text="Room Details")

    room_tree = ttk.Treeview(room_tab, columns=("Room ID", "Type", "Price", "Condition", "Status", "View", "Amenities"), show="headings")
    room_tree.pack(fill=BOTH, expand=True)
    for col in room_tree["columns"]:
        room_tree.heading(col, text=col)
        room_tree.column(col, width=150, anchor=CENTER)

    # Populate Room Details
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Room")
        rows = cursor.fetchall()
        for row in rows:
            room_tree.insert("", "end", values=row)
        conn.close()

    # Tab for Guest Details
    guest_tab = Frame(notebook)
    notebook.add(guest_tab, text="Guest Details")

    guest_tree = ttk.Treeview(guest_tab, columns=("Guest ID", "Name", "Phone", "Email"), show="headings")
    guest_tree.pack(fill=BOTH, expand=True)
    for col in guest_tree["columns"]:
        guest_tree.heading(col, text=col)
        guest_tree.column(col, width=150, anchor=CENTER)

    # Populate Guest Details
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Guest")
        rows = cursor.fetchall()
        for row in rows:
            guest_tree.insert("", "end", values=row)
        conn.close()
        # Tab for Guest-to-Room Mapping
    mapping_tab = Frame(notebook)
    notebook.add(mapping_tab, text="Guest-Room Mapping")

    mapping_tree = ttk.Treeview(mapping_tab, columns=("Guest ID", "Guest Name", "Room ID", "Room Type", "Check-In Date", "Check-Out Date"), show="headings")
    mapping_tree.pack(fill=BOTH, expand=True)

    # Define Columns
    for col in mapping_tree["columns"]:
        mapping_tree.heading(col, text=col)
        mapping_tree.column(col, width=150, anchor=CENTER)

    # Populate Guest-Room Mapping Details
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                g.guest_id, g.guest_name, b.room_id, r.room_type, b.check_in_date, b.check_out_date
            FROM 
                Guest g
            JOIN 
                Booking b ON g.guest_id = b.guest_id
            JOIN 
                Room r ON b.room_id = r.room_id
        """)
        rows = cursor.fetchall()
        for row in rows:
            mapping_tree.insert("", "end", values=row)
        conn.close()


# View Rooms
def view_rooms():
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Room")
        rows = cursor.fetchall()
        for i in tree.get_children():
            tree.delete(i)
        for row in rows:
            tree.insert("", "end", values=row)
        conn.close()

# Add Room
def add_room():
    def submit_room():
        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO Room (room_type, price, room_condition, status, room_view, amenities) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        room_type_var.get(),
                        float(price_var.get()),
                        condition_var.get(),
                        status_var.get(),
                        view_var.get(),
                        amenities_var.get(),
                    ),
                )
                conn.commit()
                messagebox.showinfo("Success", "Room added successfully!")
                add_window.destroy()
                view_rooms()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    add_window = Toplevel(root)
    add_window.title("Add Room")
    add_window.geometry("400x400")

    Label(add_window, text="Room Type").pack(pady=5)
    room_type_var = StringVar()
    Entry(add_window, textvariable=room_type_var).pack()

    Label(add_window, text="Price").pack(pady=5)
    price_var = StringVar()
    Entry(add_window, textvariable=price_var).pack()

    Label(add_window, text="Condition").pack(pady=5)
    condition_var = StringVar()
    Entry(add_window, textvariable=condition_var).pack()

    Label(add_window, text="Status").pack(pady=5)
    status_var = StringVar()
    Entry(add_window, textvariable=status_var).pack()

    Label(add_window, text="View").pack(pady=5)
    view_var = StringVar()
    Entry(add_window, textvariable=view_var).pack()

    Label(add_window, text="Amenities").pack(pady=5)
    amenities_var = StringVar()
    Entry(add_window, textvariable=amenities_var).pack()

    Button(add_window, text="Submit", command=submit_room).pack(pady=10)

# check in
def check_in():
    def submit_check_in():
        guest_id = guest_id_var.get()
        room_id = room_id_var.get()
        if not guest_id or not room_id:
            messagebox.showerror("Input Error", "Please provide both Guest ID and Room ID.")
            return

        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Room SET status = 'Occupied' WHERE room_id = %s", (room_id,))
                cursor.execute(
                    "INSERT INTO Booking (guest_id, room_id, check_in_date) VALUES (%s, %s, CURDATE())",
                    (guest_id, room_id)
                )
                conn.commit()
                messagebox.showinfo("Success", f"Guest {guest_id} checked into Room {room_id} successfully!")
                check_in_window.destroy()
                view_rooms()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    check_in_window = Toplevel(root)
    check_in_window.title("Check-In")
    check_in_window.geometry("300x200")

    Label(check_in_window, text="Guest ID").pack(pady=5)
    guest_id_var = StringVar()
    Entry(check_in_window, textvariable=guest_id_var).pack()

    Label(check_in_window, text="Room ID").pack(pady=5)
    room_id_var = StringVar()
    Entry(check_in_window, textvariable=room_id_var).pack()

    Button(check_in_window, text="Submit", command=submit_check_in).pack(pady=10)

def check_out():
    def submit_check_out():
        room_id = room_id_var.get()
        if not room_id:
            messagebox.showerror("Input Error", "Please provide a Room ID.")
            return

        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Room SET status = 'Vacant' WHERE room_id = %s", (room_id,))
                cursor.execute("UPDATE Booking SET check_out_date = CURDATE() WHERE room_id = %s AND check_out_date IS NULL", (room_id,))
                conn.commit()
                messagebox.showinfo("Success", f"Room {room_id} successfully checked out!")
                check_out_window.destroy()
                view_rooms()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    check_out_window = Toplevel(root)
    check_out_window.title("Check-Out")
    check_out_window.geometry("300x150")

    Label(check_out_window, text="Room ID").pack(pady=5)
    room_id_var = StringVar()
    Entry(check_out_window, textvariable=room_id_var).pack()

    Button(check_out_window, text="Submit", command=submit_check_out).pack(pady=10)

# Main GUI Window
root = Tk()
root.title("Hotel Management System")
root.geometry("1400x800")

# Title
Label(root, text="Hotel Management System", font=("Arial", 24)).pack(pady=10)

# Treeview for displaying rooms
tree = ttk.Treeview(root, columns=("Room ID", "Type", "Price", "Condition", "Status", "View", "Amenities"), show="headings")
tree.pack(pady=20, fill="x")
for col in tree["columns"]:
    tree.heading(col, text=col)

# Buttons
frame = Frame(root)
frame.pack(pady=20)

Button(frame, text="View All Details", command=view_all_details).pack(side=LEFT, padx=10)
Button(frame, text="View Rooms", command=view_rooms).pack(side=LEFT, padx=10)
Button(frame, text="Add Room", command=add_room).pack(side=LEFT, padx=10)
Button(frame, text="Check-In", command=check_in).pack(side=LEFT, padx=10)
Button(frame, text="Check-Out", command=check_out).pack(side=LEFT, padx=10)

# Run the application
root.mainloop()
