import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess, sys, threading, os

# Global variables to store file paths
template_file = ""
data_file = ""

def browse_template():
    global template_file
    file_path = filedialog.askopenfilename(
        title="Select Template File",
        filetypes=(("Excel Files", "*.xlsx;*.xls"), ("All Files", "*.*"))
    )
    if file_path:
        template_file = file_path
        template_label.config(text=f"Template File: {file_path}")
    return file_path

def browse_data():
    global data_file
    file_path = filedialog.askopenfilename(
        title="Select Data File",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
    )
    if file_path:
        data_file = file_path
        data_label.config(text=f"Data File: {file_path}")
    return file_path

def run_mapping():
    # Read vendor code from the entry field
    vendor_code = vendor_entry.get().strip()
    
    # Check that both files and vendor code are provided
    if not template_file or not data_file or not vendor_code:
        message_label.config(text="✘ Please select both files and enter a Vendor File Code!", fg="#777")
        return

    # Disable the Run button during processing and clear any previous message
    run_button.config(state="disabled")
    message_label.config(text="")
    
    # Start the mapping process in a separate thread so that the UI stays responsive
    threading.Thread(target=run_mapping_thread, args=(vendor_code,), daemon=True).start()

def run_mapping_thread(vendor_code):
    # Determine which script to run based on the dropdown selection
    product = product_var.get()
    if product == "Enr":
        script_to_run = "enrollment load v2.py"
    elif product == "Med":
        script_to_run = "medical load v2.py"
    elif product == "Rx":
        script_to_run = "pharmacy load v2.py"
    else:
        script_to_run = "pharmacy load.py"

    # Locate the script. When frozen, use sys._MEIPASS.
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    
    script_path = os.path.join(bundle_dir, script_to_run)
    
    try:
        # Run the selected script passing the file paths and vendor code as arguments
        result = subprocess.run(
            [sys.executable, script_path, template_file, data_file, vendor_code],
            capture_output=True, text=True
        )
        print("Script Output:", result.stdout)
        print("Script Error:", result.stderr)
        # On completion, re-enable the Run button and inform the user
        root.after(0, mapping_complete, True)
    except Exception as e:
        print("Error running script:", e)
        root.after(0, mapping_complete, False)

def mapping_complete(success):
    run_button.config(state="normal")
    if success:
        message_label.config(text="✓ Mapping completed successfully!", fg="#777")
    else:
        message_label.config(text="✘ An error occurred during mapping.", fg="#777")

# Set up the main window
root = tk.Tk()
root.title("Mapping Tool")
root.geometry("500x575")
root.configure(bg="#f5f5f5")
root.eval('tk::PlaceWindow . center')  # Center the window

# Use a modern font
import tkinter.font as tkFont
font = tkFont.Font(family="Helvetica", size=12, weight="bold")

# Header label
header_label = tk.Label(root, text="Mapping Tool", font=("Helvetica", 18, "bold"), fg="#333", bg="#f5f5f5")
header_label.pack(pady=20)

# TOP SECTION: A frame with two rows for Vendor File Code and Product Type titles and their fields.
top_section = tk.Frame(root, bg="#f5f5f5")
top_section.pack(pady=10, fill="x", padx=20)

# Configure grid to equally space two columns
top_section.columnconfigure(0, weight=1)
top_section.columnconfigure(1, weight=1)

# Row 1: Title labels
vendor_title = tk.Label(top_section, text="Vendor File Code:", font=font, bg="#f5f5f5", fg="#555")
vendor_title.grid(row=0, column=0, sticky="ew", padx=5)
product_title = tk.Label(top_section, text="Select Product Type:", font=font, bg="#f5f5f5", fg="#555")
product_title.grid(row=0, column=1, sticky="ew", padx=5)

# Row 2: Input field and dropdown
vendor_entry = tk.Entry(top_section, font=font, width=15)
vendor_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=(5, 0))
product_var = tk.StringVar(value="Enr")
product_dropdown = tk.OptionMenu(top_section, product_var, "Enr", "Med", "Rx")
product_dropdown.config(font=font, width=15)
product_dropdown.grid(row=1, column=1, sticky="ew", padx=5, pady=(5, 0))

# Instruction label for file selection (placed just below the top section)
instruction_label = tk.Label(root, text="Select your files:", font=font, bg="#f5f5f5", fg="#555")
instruction_label.pack(pady=10)

# Helper function to create buttons with the requested visual styling
def create_button(text, command, width=20):
    return tk.Button(
        root,
        text=text,
        command=command,
        font=font,
        width=width,
        relief="solid",
        bd=2,
        fg="white",
        bg="#293c5b",
        activebackground="#1f2e45",
        activeforeground="white",
        highlightthickness=0,
        pady=10,
        padx=10
    )

# Browse Template button
browse_template_button = create_button("Browse Template", browse_template)
browse_template_button.pack(pady=10)

# Label for selected template file (with wrapping and padding)
template_label = tk.Label(root, text="Template File: None", font=font, bg="#f5f5f5", fg="#777",
                          wraplength=450, justify="center", padx=10)
template_label.pack(pady=5)

# Browse Data button
browse_data_button = create_button("Browse Data", browse_data)
browse_data_button.pack(pady=10)

# Label for selected data file (with wrapping and padding)
data_label = tk.Label(root, text="Data File: None", font=font, bg="#f5f5f5", fg="#777",
                      wraplength=450, justify="center", padx=10)
data_label.pack(pady=5)

# Bottom frame to hold the Run button and feedback message
bottom_frame = tk.Frame(root, bg="#f5f5f5")
bottom_frame.pack(side="bottom", fill="x", pady=(20, 10))

# Run button (fixed in the bottom frame)
run_button = create_button("Run", run_mapping)
run_button.pack(in_=bottom_frame, pady=(0,10))

# Message label for feedback (below the Run button)
message_label = tk.Label(bottom_frame, text="", font=font, bg="#f5f5f5", fg="#777",
                         wraplength=450, justify="center")
message_label.pack()

root.eval('tk::PlaceWindow . center')
root.mainloop()
