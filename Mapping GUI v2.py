import customtkinter as ctk
from tkinter import filedialog
import subprocess, sys, threading, os
from PIL import Image  # For loading images


# Global variables to store file paths
template_file = ""
data_file = ""


# Pulling the files/file names
def browse_template():
    global template_file
    file_path = filedialog.askopenfilename(
        title="Select Template File",
        filetypes=(("Excel Files", "*.xlsx;*.xls"), ("All Files", "*.*"))
    )
    if file_path:
        template_file = file_path
        template_label.configure(text=f"Template File: {file_path}")
    return file_path

def browse_data():
    global data_file
    file_path = filedialog.askopenfilename(
        title="Select Data File",
        filetypes=(
            ("CSV Files", "*.csv"),
            ("Excel Files", "*.xlsx *.xls"),
            ("All Files", "*.*")
        )
    )
    if file_path:
        data_file = file_path
        data_label.configure(text=f"Data File: {file_path}")
    return file_path

def clear_files(*args):
    global template_file, data_file
    template_file = ""
    data_file = ""
    template_label.configure(text="Template File: None")
    data_label.configure(text="Data File: None")

def run_mapping():
    vendor_code = vendor_entry.get().strip()
    if not template_file or not data_file or not vendor_code:
        message_label.configure(text="✘ Select both files and enter a Vendor File Code", text_color="#777")
        return

    run_button.configure(state="disabled")
    message_label.configure(text="")
    threading.Thread(target=run_mapping_thread, args=(vendor_code,), daemon=True).start()


# # # Add new product # # #
def run_mapping_thread(vendor_code):
    product = product_var.get()
    if product == "Enrollment":
        script_to_run = "enrollment load v2.py"
    elif product == "Medical":
        script_to_run = "medical load v2.py"
    elif product == "Pharmacy":
        script_to_run = "pharmacy load v2.py"
    elif product == "Medical":
        script_to_run = "medical load v2.py"
    elif product == "Point Solution":
        script_to_run = "point solution load.py"
    elif product == "Biometrics":
        script_to_run = "biometrics load v2.py"
    else:
        script_to_run = "pharmacy load.py"

    try:
        result = subprocess.run(
            ["python", script_to_run, template_file, data_file, vendor_code],
            capture_output=True, text=True
        )
        print("Script Output:", result.stdout)
        print("Script Error:", result.stderr)
        root.after(0, mapping_complete, True)
    except Exception as e:
        print("Error running script:", e)
        root.after(0, mapping_complete, False)


# Add text for success/fail of mapping populating
def mapping_complete(success):
    run_button.configure(state="normal")
    if success:
        message_label.configure(text="✓ Mapping completed successfully", text_color="#777", font=bold_font)
    else:
        message_label.configure(text="✘ An error occurred during mapping", text_color="#777", font=bold_font)


# Add switch for light/dark mode
def toggle_appearance():
    mode = ctk.get_appearance_mode()
    new_mode = "Light" if mode == "Dark" else "Dark"
    ctk.set_appearance_mode(new_mode)
    update_colors(new_mode.lower())


# Adjust the colors for UI (both light and dark)
def update_colors(mode):
    """Update color theme dynamically."""
    if mode == "dark":
        outer_frame.configure(fg_color="#2B2B2B")
        top_section.configure(fg_color="#333333")
        bottom_frame.configure(fg_color="#333333")  

        browse_template_button.configure(text_color="white")
        browse_data_button.configure(text_color="white")
        run_button.configure(text_color="white")

        product_dropdown.configure(text_color="white", button_color="#444", button_hover_color="#555")
    
    # When light mode
    else:
        outer_frame.configure(fg_color="#FFFFFF")  
        top_section.configure(fg_color="#F0F0F0") 
        bottom_frame.configure(fg_color="#F0F0F0")  

        browse_template_button.configure(text_color="white")
        browse_data_button.configure(text_color="white")
        run_button.configure(text_color="white")

        product_dropdown.configure(text_color="white", button_color="#444", button_hover_color="#555")


# Set appearance and theme based on system settings
ctk.set_appearance_mode("system") 
ctk.set_default_color_theme("blue")



root = ctk.CTk()
root.title("Mapping Tool")

# Set fixed size and disable resizing
root.resizable()  # Completely disable resizing
root.update_idletasks()  # Ensure all geometry changes take effect

# Force the window to stay at exact dimensions even if maximized
# def enforce_size(event=None):
root.geometry("420x475")  

# Define a bold font for buttons, drop-down, and feedback message
bold_font = ("Helvetica", 12, "bold")

# Create an outer frame that wraps the entire app with a dark grey background.
outer_frame = ctk.CTkFrame(root, fg_color="#2B2B2B")
outer_frame.pack(fill="both", expand=True)  # Ensure proper layout handling

# HEADER: Create a header label and place an appearance switch in the top-right.
header_label = ctk.CTkLabel(outer_frame, text="Mapping Tool", font=("Helvetica", 18, "bold"))
header_label.pack(pady=20)

# Create a frame for the Appearance switch in the top-right.
appearance_frame = ctk.CTkFrame(outer_frame, fg_color="transparent", width=100, height=70)
appearance_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-40, y=20)

appearance_label = ctk.CTkLabel(appearance_frame, text="Appearance", font=bold_font)
appearance_label.pack(pady=(0,20))

appearance_switch = ctk.CTkSwitch(appearance_frame, text="", font=bold_font, command=toggle_appearance)
appearance_switch.place(relx=1.0, rely=0.0, anchor="s", x=0, y=45)

# TOP SECTION: Frame for Vendor File Code and Product Type with extra internal padding.
top_section = ctk.CTkFrame(outer_frame, fg_color="#333333")
top_section.pack(pady=10, fill="x", padx=20)
top_section.grid_columnconfigure(0, weight=1)
top_section.grid_columnconfigure(1, weight=1)

# Row 1: Title labels with added internal padding.
vendor_title = ctk.CTkLabel(top_section, text="Vendor File Code:", font=("Helvetica", 12, "bold"))
vendor_title.grid(row=0, column=0, padx=(10, 10), pady=(10, 5), sticky="ew")
product_title = ctk.CTkLabel(top_section, text="Select Product Type:", font=("Helvetica", 12, "bold"))
product_title.grid(row=0, column=1, padx=(10, 10), pady=(10, 5), sticky="ew")

# Row 2: Input field and drop‑down with extra padding inside the boxes.
vendor_entry = ctk.CTkEntry(top_section, placeholder_text="Enter vendor code", font=("Helvetica", 12, "bold"))
vendor_entry.grid(row=1, column=0, padx=(10, 10), pady=(5, 10), sticky="ew")
product_var = ctk.StringVar(value="Enrollment")

##### Add new product

# product_dropdown = ctk.CTkOptionMenu(
    # top_section, 
    # variable=product_var,
    # values=["Enrollment", "Medical", "Pharmacy"],
    # font=bold_font,
   #  width=200,  # Ensure enough space
    # anchor="center",  # Center-align text inside dropdown
# )
# product_dropdown.grid(row=1, column=1, padx=(10, 10), pady=(5, 10), sticky="ew")

product_dropdown = ctk.CTkOptionMenu(top_section, variable=product_var, font=("Helvetica", 12, "bold"),
                                      values=["Enrollment", "Medical", "Pharmacy", "Point Solution", "Biometrics"])
# product_dropdown.pack(pady=20)
product_dropdown.grid(row=1, column=1, padx=(10, 10), pady=(5, 10), sticky="ew")
product_var.trace_add("write", clear_files)
# root.update_idletasks()


# Instruction label for file selection.
instruction_label = ctk.CTkLabel(outer_frame, text="Select your files:", font=("Helvetica", 12, "bold"))
instruction_label.pack(pady=0)

# Buttons for browsing files.
browse_template_button = ctk.CTkButton(outer_frame,
                                       text="Browse Template",
                                       command=browse_template,
                                       width=200,
                                       font=bold_font)
browse_template_button.pack(pady=10)

template_label = ctk.CTkLabel(outer_frame, text="Template File: None", font=("Helvetica", 12),
                              wraplength=400, justify="center")
template_label.pack(pady=5)

browse_data_button = ctk.CTkButton(outer_frame,
                                   text="Browse Data",
                                   command=browse_data,
                                   width=200,
                                   font=bold_font)
browse_data_button.pack(pady=10)

data_label = ctk.CTkLabel(outer_frame, text="Data File: None", font=("Helvetica", 12),
                          wraplength=400, justify="center")
data_label.pack(pady=5)

# BOTTOM SECTION: Frame for the Run button and feedback message with a reduced fixed width.
bottom_frame = ctk.CTkFrame(outer_frame, fg_color="#333333", width=305)
bottom_frame.pack(pady=10, padx=20)
bottom_frame.pack_propagate(False)  # Prevent the frame from resizing to its contents

# Layout for Run button and feedback message inside the bottom frame.
run_button = ctk.CTkButton(bottom_frame, text="Run", command=run_mapping, width=200, font=bold_font)
run_button.pack(pady=(10, 5), anchor="center")
message_label = ctk.CTkLabel(bottom_frame, text="", font=bold_font, wraplength=350, justify="center")
message_label.pack(pady=(5, 10), anchor="center")

# OPTIONAL: Adding watermark images using CustomTkinter's CTkImage.
try:
    # Load the images using Pillow's Image.open and create a CTkImage with a set size.
    watermark_img_nw = ctk.CTkImage(Image.open("Innovu Text v2.png"), size=(100, 60))
    watermark_label_nw = ctk.CTkLabel(outer_frame, image=watermark_img_nw, text="")
    watermark_label_nw.place(relx=0.05, rely=0.155, anchor="sw")

    watermark_img_se = ctk.CTkImage(Image.open("Inn. Logo (no back).png"), size=(25, 25))
    watermark_label_se = ctk.CTkLabel(outer_frame, image=watermark_img_se, text="")
    watermark_label_se.place(relx=0.98, rely=0.98, anchor="se")
except Exception as e:
    print("Error loading images:", e)

root.eval('tk::PlaceWindow . center')
# root.bind("<Configure>", enforce_size)  # Prevent any size change

root.mainloop()
