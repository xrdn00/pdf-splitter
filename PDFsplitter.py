import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import os

class PDFsplitter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PDF Split")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        app_width = 1280
        app_height = 500
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        self.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
        self.iconbitmap("split.ico") 

        self.pdf_file = None  # To store the uploaded PDF file
        self.pages = None  # Store the total pages of the uploaded PDF

        # Create a main frame for the entire layout
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame to display PDF info (name and pages)
        self.info_frame = tk.Frame(self.main_frame, bd=2, highlightthickness=2)
        self.info_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.pdf_info_label = tk.Label(self.info_frame, text="No PDF file uploaded", anchor="w", justify="left", font=("Arial", 18))
        self.pdf_info_label.pack(padx=10, pady=10, fill=tk.X)

        # Create a frame for the sidebar and the 2 buttons above it
        self.sidebar_container_frame = tk.Frame(self.main_frame, bd=2, relief="solid", highlightbackground="blue", highlightthickness=2)
        self.sidebar_container_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Create the buttons inside the sidebar
        self.button1 = tk.Button(self.sidebar_container_frame, text="Upload PDF", command=self.upload_pdf)
        self.button1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.button2 = tk.Button(self.sidebar_container_frame, text="Add Page Range", command=self.add_form)
        self.button2.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.button3 = tk.Button(self.sidebar_container_frame, text="Extract individual page", command=self.extract_pdf_pages, state=tk.DISABLED)  # Disabled by default
        self.button3.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.split_button = tk.Button(self.sidebar_container_frame, text="Split and Save As", command=self.split_pdf, state=tk.DISABLED)
        self.split_button.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # Create a canvas for the sidebar
        self.canvas = tk.Canvas(self.sidebar_container_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Create a vertical scrollbar for the canvas
        self.scrollbar = tk.Scrollbar(self.sidebar_container_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the sidebar content
        self.sidebar_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.sidebar_frame, anchor="nw")

        # Update the scroll region whenever the sidebar content changes
        def update_scroll_region(event=None):
            self.canvas.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.sidebar_frame.bind("<Configure>", update_scroll_region)

        # List to track the form frames added
        self.form_frames = []

        # Counter to keep track of the number of forms added
        self.form_counter = 1

    def upload_pdf(self):
        """Allow the user to upload a PDF file."""
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.pdf_file = file_path
            with open(self.pdf_file, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                self.pages = len(reader.pages)
            
            pdf_name = os.path.basename(self.pdf_file)
            self.pdf_info_label.config(text=f"PDF file name: {pdf_name}\nPages: {self.pages}")
            print(f"PDF uploaded successfully with {self.pages} pages.")

            self.split_button.config(state=tk.NORMAL)
            self.button3.config(state=tk.NORMAL)

        else:
            self.split_button.config(state=tk.DISABLED)
            self.button3.config(state=tk.DISABLED)

    def add_form(self):
        """Add a new form for a page range."""
        form_frame = tk.Frame(self.sidebar_frame, pady=10, bd=2, relief="solid", highlightbackground="blue", highlightthickness=2)
        form_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        label_file_name = tk.Label(form_frame, text="File Name:")
        label_file_name.pack(side=tk.TOP, fill=tk.X)

        file_name_entry = tk.Entry(form_frame, width=47, borderwidth=2, relief="solid")
        file_name_entry.pack(side=tk.TOP, fill=tk.X, padx=5)

        label = tk.Label(form_frame, text=f"Page Range {self.form_counter}")
        label.pack(side=tk.TOP, fill=tk.X)

        entry_frame1 = tk.Frame(form_frame)
        entry_frame1.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

        label1 = tk.Label(entry_frame1, text="Start Page:")
        label1.pack(side=tk.LEFT)

        entry1 = tk.Entry(entry_frame1, width=47)
        entry1.pack(side=tk.LEFT, fill=tk.X, padx=5)

        entry_frame2 = tk.Frame(form_frame)
        entry_frame2.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

        label2 = tk.Label(entry_frame2, text="End Page: ")
        label2.pack(side=tk.LEFT)

        entry2 = tk.Entry(entry_frame2, width=47)
        entry2.pack(side=tk.LEFT, fill=tk.X, padx=5)

        remove_button = tk.Button(form_frame, text="Remove", command=lambda: self.remove_form(form_frame))
        remove_button.pack(side=tk.TOP, pady=5)

        self.form_frames.append((form_frame, file_name_entry, entry1, entry2))
        self.form_counter += 1

        self.sidebar_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def remove_form(self, form_frame):
        """Remove a specific form."""
        form_frame.destroy()
        self.form_frames = [f for f in self.form_frames if f[0] != form_frame]
        self.sidebar_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def split_pdf(self):
        """Split the uploaded PDF based on the page ranges entered in the forms."""
        if not self.pdf_file:
            messagebox.showwarning("No PDF", "Please upload a PDF file first.")
            return

        # Check if there are any valid page rangesW
        if not self.form_frames:
            messagebox.showwarning("No Page Ranges", "Please add at least one page range before splitting.")
            return

        # Remove incomplete or invalid forms
        for form_frame, file_name_entry, entry1, entry2 in self.form_frames:
            start_page = entry1.get().strip()
            end_page = entry2.get().strip()
            file_name = file_name_entry.get().strip()

            # Check if the form has empty fields
            if not start_page or not end_page or not file_name:
                messagebox.showwarning("Incomplete Page Range", "Please fill out the file name, start page, and end page for each range.")
                return

            try:
                start_page = int(start_page) - 1  # Convert to 0-based index
                end_page = int(end_page) - 1  # Convert to 0-based index

                # Ensure the page range is valid
                if start_page < 0 or end_page >= self.pages or start_page > end_page:
                    messagebox.showwarning("Invalid Page Range", "Please enter a valid page range.")
                    return

            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter valid numeric values for both start and end pages.")
                return

        # Ask the user for a folder to save the split files
        save_folder = filedialog.askdirectory(title="Select Folder to Save Split PDFs")
        if not save_folder:
            print("No folder selected, exiting PDF split.")
            return

        # Open the uploaded PDF
        with open(self.pdf_file, "rb") as f:
            reader = PyPDF2.PdfReader(f)

            # Iterate through each form and split the PDF based on the entered page range
            for form_frame, file_name_entry, entry1, entry2 in self.form_frames:
                start_page = int(entry1.get()) - 1  # Convert to 0-based index
                end_page = int(entry2.get()) - 1  # Convert to 0-based index
                file_name = file_name_entry.get().strip()

                # Create a PDF writer to save the split pages
                writer = PyPDF2.PdfWriter()

                for page_num in range(start_page, end_page + 1):
                    writer.add_page(reader.pages[page_num])

                # Save the split PDF to the selected folder using the provided file name
                output_filename = os.path.join(save_folder, f"{file_name} - pages {start_page + 1} to {end_page + 1}.pdf")
                with open(output_filename, "wb") as output_pdf:
                    writer.write(output_pdf)

                print(f"PDF split saved as {output_filename}")

        # After all splits are done, show a success message box
        messagebox.showinfo("Success", "PDF has been successfully split and saved!")

    def extract_pdf_pages(self):
        # Ensure that a PDF file is uploaded before allowing page extraction
        if not self.pdf_file:
            messagebox.showwarning("No PDF", "Please upload a PDF file first.")
            return

        # Ask the user for a folder to save the extracted pages
        save_folder = filedialog.askdirectory(title="Select Folder to Save Pages")
        if not save_folder:
            print("No folder selected, exiting PDF extraction.")
            return
        
        # Open the input PDF file in read-binary mode
        with open(self.pdf_file, "rb") as input_pdf:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(input_pdf)
            
            # Iterate through all the pages
            for page_num in range(len(pdf_reader.pages)):
                # Create a PDF writer object
                pdf_writer = PyPDF2.PdfWriter()
                
                # Extract the specific page
                pdf_writer.add_page(pdf_reader.pages[page_num])
                
                # Define the output file name based on the page number
                output_pdf_path = os.path.join(save_folder, f"Page_{page_num + 1}.pdf")
                
                # Write the single page to a new PDF file
                with open(output_pdf_path, "wb") as output_pdf:
                    pdf_writer.write(output_pdf)
                
                print(f"Page {page_num + 1} has been saved as {output_pdf_path}")

        # After all pages are extracted, show a success message box
        messagebox.showinfo("Success", "PDF pages have been successfully extracted and saved!")

if __name__ == "__main__":
    app = PDFsplitter()
    app.mainloop()
