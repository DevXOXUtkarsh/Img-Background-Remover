import requests
from io import BytesIO
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# API key for remove.bg
API_KEY = 'M83k83KPPzsnDQKvTuXoJbBw'

def remove_background(api_key, input_path, output_path):
    try:
        # Open the input image
        with open(input_path, 'rb') as file:
            image_data = file.read()

        # Define the API endpoint and headers
        url = 'https://api.remove.bg/v1.0/removebg'
        headers = {'X-Api-Key': api_key}

        # Send the image data to the API
        response = requests.post(url, headers=headers, files={'image_file': ('image.jpg', image_data)})

        # Check if the request was successful
        if response.status_code == 200:
            # Convert the byte data to an image
            img = Image.open(BytesIO(response.content))
            # Save the image with transparent background
            img.save(output_path)
            messagebox.showinfo("Success", f"Background removed and image saved to {output_path}")
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.text}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def start_processing():
    input_path = input_entry.get()
    output_path = output_entry.get()
    if input_path and output_path:
        remove_background(API_KEY, input_path, output_path)
    else:
        messagebox.showerror("Error", "Please select both input and output paths")

# Create the main window
root = tk.Tk()
root.title("Background Remover")

# Input file selection
input_label = tk.Label(root, text="Select Input Image:")
input_label.grid(row=0, column=0, padx=10, pady=5)
input_entry = tk.Entry(root, width=40)
input_entry.grid(row=0, column=1, padx=10, pady=5)
input_button = tk.Button(root, text="Browse", command=select_input_file)
input_button.grid(row=0, column=2, padx=10, pady=5)

# Output file selection
output_label = tk.Label(root, text="Select Output Image:")
output_label.grid(row=1, column=0, padx=10, pady=5)
output_entry = tk.Entry(root, width=40)
output_entry.grid(row=1, column=1, padx=10, pady=5)
output_button = tk.Button(root, text="Browse", command=select_output_file)
output_button.grid(row=1, column=2, padx=10, pady=5)

# Start button
start_button = tk.Button(root, text="Remove Background", command=start_processing)
start_button.grid(row=2, column=1, padx=10, pady=20)

# Run the Tkinter event loop
root.mainloop()

