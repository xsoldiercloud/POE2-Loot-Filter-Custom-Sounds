import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def update_loot_filter(filter_file, item_name, sound_file):
    # Map the item names to their respective headers
    headers = {
        "Divine": "## Divine Orb Style",
        "Exalted Orb": "# Currency Tier B: Exalt"
    }
    if item_name not in headers:
        raise ValueError(f"Unsupported item name: {item_name}")

    # Create a new file name for the custom loot filter
    filter_dir = os.path.dirname(filter_file)
    original_name = os.path.basename(filter_file)
    custom_name = original_name.replace(".filter", "_custom.filter")
    custom_filter_path = os.path.join(filter_dir, custom_name)

    # Check if the custom filter file already exists
    if os.path.exists(custom_filter_path):
        response = messagebox.askyesno(
            "File Exists",
            f"The file '{custom_name}' already exists. Do you want to overwrite it?"
        )
        if not response:
            messagebox.showinfo("Operation Canceled", "No changes were made.")
            return  # Exit the function if the user chooses not to overwrite

    # Read the loot filter content
    with open(filter_file, 'r') as file:
        lines = file.readlines()

    # Detect and update the sound for the given item
    updated_lines = []
    in_section = False

    # Get the correct header for the item
    header = headers[item_name]

    for line in lines:
        # Check if the line matches the relevant header
        if header in line:
            in_section = True
            updated_lines.append(line)
            continue

        if in_section:
            # Look for PlayAlertSound or CustomAlertSound and replace/add CustomAlertSound
            if "PlayAlertSound" in line or "CustomAlertSound" in line:
                new_sound_line = f'CustomAlertSound "{os.path.basename(sound_file)}"\n'
                updated_lines.append(new_sound_line)
                in_section = False  # Exit section after updating
            else:
                updated_lines.append(line)
            continue

        # Add lines outside the relevant section unchanged
        updated_lines.append(line)

    # Save the updated content to the new filter file
    with open(custom_filter_path, 'w') as file:
        file.writelines(updated_lines)

    # Copy the sound file to the filter directory if it's not already there
    target_sound_path = os.path.join(filter_dir, os.path.basename(sound_file))
    if os.path.abspath(sound_file) != os.path.abspath(target_sound_path):
        shutil.copy(sound_file, filter_dir)

    # Notify the user
    messagebox.showinfo(
        "Success",
        f"Successfully created a new loot filter: '{custom_name}'.\n\n"
        "To use the new filter:\n"
        "1. Go to Options > Game > Item Filter in Path of Exile 2.\n"
        "2. Refresh the loot filter list.\n"
        f"3. Select '{custom_name}' from the list."
    )




def browse_filter():
    file_path = filedialog.askopenfilename(
        title="Select Loot Filter File",
        filetypes=[("Loot Filter Files", "*.filter"), ("All Files", "*.*")]
    )
    filter_entry.delete(0, tk.END)
    filter_entry.insert(0, file_path)

def browse_sound():
    file_path = filedialog.askopenfilename(
        title="Select Sound File",
        filetypes=[("OGG Sound Files", "*.ogg"), ("All Files", "*.*")]
    )
    sound_entry.delete(0, tk.END)
    sound_entry.insert(0, file_path)

def apply_changes():
    filter_file = filter_entry.get().strip()
    sound_file = sound_entry.get().strip()
    item_name = item_var.get()

    if not filter_file or not sound_file:
        messagebox.showerror("Error", "Both the loot filter and sound file paths are required.")
        return

    if not os.path.exists(filter_file):
        messagebox.showerror("Error", f"Loot filter file '{filter_file}' not found.")
        return

    if not os.path.exists(sound_file):
        messagebox.showerror("Error", f"Sound file '{sound_file}' not found.")
        return

    update_loot_filter(filter_file, item_name, sound_file)

# Initialize GUI
root = tk.Tk()
root.title("Loot Filter Customizer")

# Filter File Selection
tk.Label(root, text="Loot Filter File:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
filter_entry = tk.Entry(root, width=50)
filter_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse...", command=browse_filter).grid(row=0, column=2, padx=10, pady=10)

# Sound File Selection
tk.Label(root, text="Sound File (.ogg):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
sound_entry = tk.Entry(root, width=50)
sound_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse...", command=browse_sound).grid(row=1, column=2, padx=10, pady=10)

# Item Selection
tk.Label(root, text="Select Item:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
item_var = tk.StringVar(value="Divine")  # Default to "Divine"
tk.Radiobutton(root, text="Divine Orb", variable=item_var, value="Divine").grid(row=2, column=1, sticky="w")
tk.Radiobutton(root, text="Exalted Orb", variable=item_var, value="Exalted Orb").grid(row=3, column=1, sticky="w")

# Apply Button
tk.Button(root, text="Apply Changes", command=apply_changes).grid(row=4, column=0, columnspan=3, pady=20)

# Run GUI
root.mainloop()
