import tkinter as tk
from tkinter import PhotoImage  # For simple images like .png, .gif
from PIL import Image, ImageTk  # For more complex image formats (e.g. .jpg, .bmp)
import PDFsplitter

# Function to close the window
def close_window():
    root.destroy()  # This ensures the window is fully destroyed
    app = PDFsplitter.PDFsplitter()  # Open the main application
    app.mainloop()


# Create the main window
root = tk.Tk()

# Remove the title bar and window decorations
root.overrideredirect(True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
app_width = 500
app_height = 300
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
root.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
root.iconbitmap("split.ico") 

root.configure()

# Load your image
image_path = "logo.png"  # Replace this with the actual path of your image

# For .png, .gif images
image = PhotoImage(file=image_path)

# If you are using other formats like .jpg, use PIL to open and convert
# image = Image.open("path_to_your_image.jpg")
# image = ImageTk.PhotoImage(image)

# Create a Label widget to display the image
image_label = tk.Label(root, image=image)
image_label.pack(expand=True)

# Schedule the close_window function to be called after 5000 milliseconds (5 seconds)
root.after(5000, close_window)

# Run the Tkinter main loop
root.mainloop()
