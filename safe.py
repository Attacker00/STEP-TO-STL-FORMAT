import os
import tkinter as tk
from tkinter import filedialog

import cadquery as cq
import trimesh
from PIL import Image, ImageTk
from stl import mesh


# Function to handle file selection
def browse_file():
    # Use filedialog to select one or more files
    filenames = filedialog.askopenfilenames()
    # Update the label with the selected filenames
    file_label.config(text=", ".join(filenames))

# Function to handle file conversion
def convert():
    # Get the input filenames
    input_filenames = file_label.cget("text").split(", ")
    
    
    # Check if any files have been selected
    if input_filenames == ["No file selected."]:
        print("Please select one or more files to convert.")
    else:
        # Get the output directory
        output_directory = filedialog.askdirectory()
        
        for input_filename in input_filenames:
            # Create the output filename by replacing the file extension with ".stl"
            output_filename = os.path.splitext(os.path.basename(input_filename))[0] + ".stl"
            # Create the output file path by joining the output directory and output filename
            output_file_path = os.path.join(output_directory, output_filename)
            # Create the output text file path
            output_text_file_path = os.path.join(output_directory, output_filename + ".txt")
            
            # Import the STEP file
            try:
                afile = cq.importers.importStep(input_filename)
            except ValueError:
                print(f"STEP file {input_filename} could not be loaded")
                continue
            
            # Export the STL file
            cq.exporters.export(afile, output_file_path)
            print(f"Converted {input_filename} to {output_file_path}")
            
            # Load the STL file
            try:
                stl_mesh = trimesh.load(output_file_path)
                # Check if the mesh is watertight
                watertight = stl_mesh.is_watertight
                # Count the number of triangles
                num_triangles = stl_mesh.faces.shape[0]
                # Calculate the dimensions
                dimensions = stl_mesh.bounding_box.extents
                length, breadth, height = dimensions
                
                # Calculate the percentage of watertightness
                watertight_percent = 100.0 * stl_mesh.volume / stl_mesh.bounding_box.volume
                
                # Write the dimensions, number of triangles, watertight status, and watertight percentage to the output text file
                with open(output_text_file_path, "w") as f:
                    f.write(f"Dimensions: length : {length:.1f} x breadth : {breadth:.1f} x height : {height:.1f}\n")
                    f.write(f"Watertight percentage: {watertight_percent:.2f}%\n")
                    f.write(f"Watertight: {'Yes' if watertight else 'No'}\n")
                    f.write(f"Number of triangles: {num_triangles}\n")
                    
                print(f"Text file saved as {output_text_file_path}")
                
            except Exception as e:
                print(e)
                print(f"Error while calculating dimensions for {output_filename}")
            
        # Update the status label
        status_label.config(text=f"All selected files converted successfully.")

# Create the main window
window = tk.Tk()
window.title("File Converter")

# Load the image
image = Image.open("logo.jpg")
logo = ImageTk.PhotoImage(image)

# Create a label for the image
logo_label = tk.Label(window, image=logo)
logo_label.pack(side="top", fill="both", expand=True)

# Add a label for the selected file
file_label = tk.Label(window, text="No file selected.")
file_label.pack()

# Add a "Import" button to select a file
browse_button = tk.Button(window, text="Import", command=browse_file, width=20, height=2)
browse_button.pack(pady=10)

# Add a "Export" button to convert the selected file
convert_button = tk.Button(window, text="Export", command=convert, width=20, height=2)
convert_button.pack(pady=10)

# Add a label to show the status of the conversion
status_label = tk.Label(window, text="")
status_label.pack(pady=10)

# Center the window on the screen
window.update_idletasks()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = window.winfo_width()
window_height = window.winfo_height()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
window.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))

# Start the main loop
window.mainloop()
