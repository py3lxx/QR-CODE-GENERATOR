import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import qrcode
from PIL import Image, ImageTk

def createQR(*args):
    data = text_entry.get()
    if data:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=qr_color, back_color=bg_color)
        res_img = img.resize((280, 250))  # Resize QR Code Size

        tkimage = ImageTk.PhotoImage(res_img)
        qr_canvas.delete('all')
        qr_canvas.create_image(0, 0, anchor=tk.NW, image=tkimage)
        qr_canvas.image = tkimage
    else:
        messagebox.showwarning("Warning", 'Enter Data in Entry First')

def saveQR(*args):
    data = text_entry.get()
    if data:
        img = qrcode.make(data)  # Generate QR code  
        res_img = img.resize((280, 250))  # Resize QR Code Size
        
        path = filedialog.asksaveasfilename(defaultextension=".png",)
        if path:
            res_img.save(path)
            messagebox.showinfo("Success", "QR Code is Saved ")
    else:
        messagebox.showwarning("Warning", 'Enter Data in Entry First')

def choose_qr_color():
    global qr_color
    qr_color = colorchooser.askcolor(title="Choose QR Code Color")[1]  # Pick color

def choose_bg_color():
    global bg_color
    bg_color = colorchooser.askcolor(title="Choose Background Color")[1]  # Pick color

def choose_background_image():
    global background_photo
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        background_image = Image.open(file_path)
        background_photo = ImageTk.PhotoImage(background_image)
        background_canvas.create_image(0, 0, anchor="nw", image=background_photo)

root = tk.Tk()
root.title("QR Code Generator")
root.geometry("300x450")
root.config(bg='white')
root.resizable(0, 0)

#remove title bar
root.overrideredirect(True)

#fake title bar
title_bar = tk.Frame(root, bg="black", relief="raised", bd=5)
title_bar.pack(expand=True, fill=tk.X)  # Corrected pack parameters

def move_window(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')

# Bind the title bar to drag the window
title_bar.bind('<B1-Motion>', move_window)

# Initialize default colors
qr_color = "white"
bg_color = "black"

# Load the background image
background_image = Image.open("back.png")
background_photo = ImageTk.PhotoImage(background_image)

# Create a Canvas to place the background image
background_canvas = tk.Canvas(root, width=300, height=450)
background_canvas.pack(fill="both", expand=True)
background_canvas.create_image(0, 0, anchor="nw", image=background_photo)

frame1 = tk.Frame(root, bd=2, relief=tk.RAISED)
frame1.place(x=10, y=5, width=280, height=250)

# Create a Canvas in frame2 for the background image
frame2 = tk.Frame(root, bd=2, relief=tk.SUNKEN)
frame2.place(x=10, y=260, width=280, height=180)

# Load the button area background image
button_area_bg_image = Image.open("arka.png")
button_area_bg_photo = ImageTk.PhotoImage(button_area_bg_image)

button_canvas = tk.Canvas(frame2, width=280, height=180)
button_canvas.pack(fill="both", expand=True)
button_canvas.create_image(0, 0, anchor="nw", image=button_area_bg_photo)

coverImg = tk.PhotoImage(file="cov.png")

qr_canvas = tk.Canvas(frame1)
qr_canvas.bind("<Double-1>", saveQR)
qr_canvas.create_image(0, 0, anchor=tk.NW, image=coverImg)
qr_canvas.image = coverImg
qr_canvas.pack(fill=tk.BOTH)

def on_entry_click(event):
    if text_entry.get() == 'link':
        text_entry.delete(0, "end")  # Clear the placeholder text
        text_entry.config(foreground='grey')  # Change text color to black

def on_focus_out(event):
    if text_entry.get() == '':
        text_entry.insert(0, 'link')  # Restore the placeholder text
        text_entry.config(foreground='grey')  # Change text color to grey

# Create the entry widget with placeholder text and custom colors
text_entry = tk.Entry(frame2, width=26, font=("Sitka Small", 11), justify=tk.CENTER, fg='grey', bg='black')  # Set the text color and background color
text_entry.insert(0, 'link')  # Insert the placeholder text
text_entry.bind("<FocusIn>", on_entry_click)  # Bind click/focus event
text_entry.bind("<FocusOut>", on_focus_out)  # Bind focus out event
text_entry.bind("<Return>", createQR)  # Bind the Return key to the function
text_entry.place(x=5, y=5)


###########################################################################################

def on_enter(event):
    event.widget.config(bg="gray", fg="black")  # Change background and text color on hover

def on_leave(event):
    event.widget.config(bg="black", fg="white")  # Revert to original colors when mouse leaves

# Create the Create button
btn_1 = tk.Button(frame2, text="Create", width=10, command=createQR, bg="black", fg="white")
btn_1.place(x=25, y=90)
btn_1.bind("<Enter>", on_enter)
btn_1.bind("<Leave>", on_leave)

# Save the button
btn_2 = tk.Button(frame2, text="Save", width=10, command=saveQR, bg="black", fg="white")
btn_2.place(x=100, y=90)
btn_2.bind("<Enter>", on_enter)
btn_2.bind("<Leave>", on_leave)

# Exit the button
btn_3 = tk.Button(frame2, text="Exit", width=10, command=root.quit, bg="black", fg="white")
btn_3.place(x=175, y=90)
btn_3.bind("<Enter>", on_enter)
btn_3.bind("<Leave>", on_leave)

########################################################################################

# Create the menu bar
menu_bar = tk.Menu(root)

# Create the "Options" menu
options_menu = tk.Menu(menu_bar, tearoff=0)
options_menu.add_command(label="Change QR Code Color", command=choose_qr_color)
options_menu.add_command(label="Change Background Color", command=choose_bg_color)
options_menu.add_command(label="Change Background Image", command=choose_background_image)

# Add the "Options" menu to the menu bar
menu_bar.add_cascade(label="Options", menu=options_menu)

# Configure the root window to display the menu
root.config(menu=menu_bar)

########################################################################################

# Configure the root window to display the menu
root.config(menu=menu_bar)

# Center the window on the screen
root.update_idletasks()  # Update the window to get its width and height
window_width = root.winfo_width()
window_height = root.winfo_height()

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position to center the window
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the position
root.geometry(f'{window_width}x{window_height}+{x}+{y}')


root.mainloop()



## ALL MADE BY EGE