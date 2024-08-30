import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime

# In-memory storage for events
events = []

# Event creation
def add_event(title, description, date, time):
    try:
        event_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    except ValueError:
        messagebox.showerror("Error", "Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.")
        return
    
    new_event = {
        'title': title,
        'description': description,
        'datetime': event_datetime
    }
    
    events.append(new_event)
    messagebox.showinfo("Success", "Event added successfully.")
    update_event_list()

# Listing events
def list_events():
    if not events:
        messagebox.showinfo("Info", "No events found.")
        return
    
    sorted_events = sorted(events, key=lambda x: x['datetime'])
    
    event_list = ""
    for event in sorted_events:
        event_list += f"Title: {event['title']}\n"
        event_list += f"Description: {event['description']}\n"
        event_list += f"Date and Time: {event['datetime'].strftime('%Y-%m-%d %H:%M')}\n"
        event_list += "-" * 20 + "\n"
    
    messagebox.showinfo("Events", event_list)

# Deleting events
def delete_event():
    title = simpledialog.askstring("Delete Event", "Enter the title of the event to delete:")
    global events
    updated_events = [event for event in events if event['title'] != title]
    
    if len(updated_events) == len(events):
        messagebox.showinfo("Info", f"No event found with the title '{title}'.")
    else:
        events = updated_events
        messagebox.showinfo("Success", f"Event with title '{title}' deleted successfully.")
        update_event_list()

# Searching events
def search_events():
    keyword = simpledialog.askstring("Search Events", "Enter a keyword to search for events:")
    matching_events = [event for event in events if keyword.lower() in event['title'].lower() or keyword.lower() in event['description'].lower()]
    
    if not matching_events:
        messagebox.showinfo("Info", f"No events found with the keyword '{keyword}'.")
    else:
        event_list = ""
        for event in matching_events:
            event_list += f"Title: {event['title']}\n"
            event_list += f"Description: {event['description']}\n"
            event_list += f"Date and Time: {event['datetime'].strftime('%Y-%m-%d %H:%M')}\n"
            event_list += "-" * 20 + "\n"
        
        messagebox.showinfo("Events", f"Events matching the keyword '{keyword}':\n\n{event_list}")

# Editing events
def edit_event():
    title = simpledialog.askstring("Edit Event", "Enter the title of the event to edit:")
    event_to_edit = next((event for event in events if event['title'] == title), None)
    
    if event_to_edit:
        new_title = simpledialog.askstring("Edit Event", "New title (press Cancel for no changes):") or event_to_edit['title']
        new_description = simpledialog.askstring("Edit Event", "New description (press Cancel for no changes):") or event_to_edit['description']
        new_date = simpledialog.askstring("Edit Event", "New date (YYYY-MM-DD) (press Cancel for no changes):") or event_to_edit['datetime'].strftime('%Y-%m-%d')
        new_time = simpledialog.askstring("Edit Event", "New time (HH:MM) (press Cancel for no changes):") or event_to_edit['datetime'].strftime('%H:%M')
        
        try:
            new_datetime = datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format. Event not edited.")
            return
        
        event_to_edit['title'] = new_title
        event_to_edit['description'] = new_description
        event_to_edit['datetime'] = new_datetime
        
        messagebox.showinfo("Success", f"Event with title '{title}' edited successfully.")
        update_event_list()
    else:
        messagebox.showinfo("Info", f"No event found with the title '{title}'.")

# Update the event list display
def update_event_list():
    event_list = [f"Title: {event['title']}, Date: {event['datetime'].strftime('%Y-%m-%d %H:%M')}" for event in sorted(events, key=lambda x: x['datetime'])]
    event_listbox.delete(0, tk.END)
    for item in event_list:
        event_listbox.insert(tk.END, item)

# Create the main window
root = tk.Tk()
root.title("Event Scheduler")

# Create and place the buttons
tk.Button(root, text="Add Event", command=lambda: add_event(
    simpledialog.askstring("Add Event", "Enter event title:"),
    simpledialog.askstring("Add Event", "Enter event description:"),
    simpledialog.askstring("Add Event", "Enter event date (YYYY-MM-DD):"),
    simpledialog.askstring("Add Event", "Enter event time (HH:MM):")
)).pack(pady=5)

tk.Button(root, text="List Events", command=list_events).pack(pady=5)
tk.Button(root, text="Delete Event", command=delete_event).pack(pady=5)
tk.Button(root, text="Search Events", command=search_events).pack(pady=5)
tk.Button(root, text="Edit Event", command=edit_event).pack(pady=5)

# Create and place the event listbox
event_listbox = tk.Listbox(root, width=50, height=10)
event_listbox.pack(pady=10)

# Run the GUI event loop
root.mainloop()
