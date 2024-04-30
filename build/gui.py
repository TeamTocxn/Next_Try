from pathlib import Path
#from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, StringVar
from tkinter.ttk import Combobox, Style
import tkinter as tk
from tkinter import *
from tkinter import ttk, simpledialog, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont,ImageOps
import os
import sqlite3
import io
from openpyxl import Workbook
import tkinter.messagebox as messagebox
from tkcalendar import Calendar
from tkinter import OptionMenu
import qrcode
from PIL import Image

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"F:\Next_Try\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class StudentDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.cursor = self.conn.cursor()

        self.cur.execute('''CREATE TABLE IF NOT EXISTS students (
                            id INTEGER PRIMARY KEY,
                            roll_no INTEGER,
                            name TEXT,
                            image BLOB,
                            gender TEXT,
                            dob TEXT,
                            address TEXT,
                            phone_no TEXT,
                            email TEXT,
                            dept TEXT,
                            year TEXT,
                            identity_proof TEXT,
                            last_qualification TEXT,
                            qualification_cert BLOB,
                            identity_proof_image BLOB)''')
        self.conn.commit()

    def insert_student(self, roll_no, name, image_data, gender, dob, address, phone_no, email, dept, year, identity_proof,
                       last_qualification, qualification_cert_data, identity_proof_image_data):
        self.cur.execute(
            "INSERT INTO students (roll_no, name, image, gender, dob, address, phone_no, email, dept, year, identity_proof, last_qualification, qualification_cert, identity_proof_image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (roll_no, name, image_data, gender, dob, address, phone_no, email, dept, year, identity_proof, last_qualification,qualification_cert_data, identity_proof_image_data))
        self.conn.commit()
    def delete_student(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        self.conn.commit()
        
  
    

    def fetch_students(self):
        self.cur.execute("SELECT id, roll_no, name, gender, dob, year, dept FROM students")
        return self.cur.fetchall()

    def fetch_data_excel(self):
        self.cur.execute(
            "SELECT id, roll_no, name, gender, dob, address, phone_no, email, dept, year, identity_proof FROM students")
        return self.cur.fetchall()

    def get_image(self, student_id):
        self.cur.execute("SELECT image FROM students WHERE id=?", (student_id,))
        row = self.cur.fetchone()
        if row:
            return row[0]
        
    def get_qualification_cert(self, student_id):
        self.cur.execute("SELECT qualification_cert FROM students WHERE id=?", (student_id,))
        row = self.cur.fetchone()
        if row:
            return row[0]
        
    def get_identity_proof_image(self, student_id):
        self.cur.execute("SELECT identity_proof_image FROM students WHERE id=?", (student_id,))
        row = self.cur.fetchone()
        if row:
            return row[0]
        

 
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Database")
        self.root.resizable(False, False)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = 1450
        height = 750
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        #self.root.overrideredirect(True)
        def on_title_bar_click(event):
            # Capture mouse position when title bar is clicked
            self.x = event.x
            self.y = event.y

        def on_drag(event):
            # Move the window when dragging the title bar
            deltax = event.x - self.x
            deltay = event.y - self.y
            new_x = self.root.winfo_x() + deltax
            new_y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{new_x}+{new_y}")

        
        #close_btn.image = close_icon
        self.db = StudentDatabase("student.db")  # Initialize the database
    
                # Frames
          
        self.root_canvas = tk.Canvas(self.root, width=1450, height=750)
        self.root_canvas.pack(side="left", fill="both", expand=True)
        
                # Frames
        self.left_frame = tk.Canvas(self.root_canvas, width=1450, height=750)
        self.left_frame.pack(side="left", fill="both", expand=True)
        
        self.right_bar_frame = tk.Canvas(self.left_frame, width=250, height=750)
        self.right_bar_frame.pack(side="left", fill="both")


        self.middle_frame = tk.Canvas(self.left_frame, width=1200, height=750)
        self.middle_frame.pack(side="right", fill="both", expand=True)
        
        self.middle_Canvas = tk.Canvas(self.middle_frame, width=1200, height=750)
        self.middle_Canvas.pack(side="right", fill="both", expand=True)
      
        self.database_frame = tk.Canvas(self.middle_Canvas, width=515, height=750)
        self.database_frame.pack(side="left", fill="both")

        
        self.details_frame = tk.Canvas(self.middle_Canvas, width=685, height=750,bg="#FFFFFF")
        self.details_frame.pack(side="right", fill="both",expand=True)
        
        

        
             
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.canvas = Canvas(
            self.right_bar_frame,
            bg = "#FFFFFF",
            height = 750,
            width = 250,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        
        self.left_bar = Canvas(
            self.canvas,
            bg="#152364",
            height = 950,
            width = 300,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        

        self.left_bar.place(x = 0, y = 0)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
           
        self.image_logo = PhotoImage(
            file=relative_to_assets("tocxn.png"))
        
        self.left_bar.create_image(124, 95, image=self.image_logo)
        self.left_bar.bind("<Button-1>", on_title_bar_click)
        self.left_bar.bind("<B1-Motion>", on_drag)
        
       
       
        self.add_group_1 = PhotoImage(
            file=relative_to_assets("add_1.png"))
        self.add_group_2 = PhotoImage(
            file=relative_to_assets("add_2.png"))
    
        
        
        def add_bttn(img1, img2):
            mybtn = Button(self.left_bar, border=0, cursor='hand2', bg="#152364", activebackground="#152364",relief=SUNKEN)
            image_a = img1
            image_b = img2

            def on_enter(e):
                mybtn['image'] = image_b

            def on_leave(e):
                mybtn['image'] = image_a

            mybtn.image_normal = image_a
            mybtn.image_hover = image_b
            mybtn['image'] = mybtn.image_normal
            # Initially show the hover image
            
            mybtn.bind("<Enter>", on_enter)
            mybtn.bind("<Leave>", on_leave)
            mybtn.place(x=18, y=225)
            mybtn.config(command=self.add_student)

    
        add_bttn(self.add_group_1, self.add_group_2)
        
          
        self.delete_group_1 = PhotoImage(
            file=relative_to_assets("delete_1.png"))
        self.delete_group_2 = PhotoImage(
            file=relative_to_assets("delete_2.png"))
        
        
        def delete_bttn(img1, img2):
            mybtn1 = Button(self.left_bar, border=0, cursor='hand2', bg="#152364", activebackground="#152364",relief=SUNKEN)
            image_a = img1
            image_b = img2

            def on_enter(e):
                mybtn1['image'] = image_b

            def on_leave(e):
                mybtn1['image'] = image_a

            mybtn1.image_normal = image_a
            mybtn1.image_hover = image_b
            mybtn1['image'] = mybtn1.image_normal
            # Initially show the hover image            
            mybtn1.bind("<Enter>", on_enter)
            mybtn1.bind("<Leave>", on_leave)
            mybtn1.place(x=18, y=305)
            mybtn1.config(command=self.delete_selected_student)
        
        
        delete_bttn(self.delete_group_1, self.delete_group_2)
       #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        
        self.generate_id_1 = PhotoImage(
            file=relative_to_assets("generate_id_1.png"))
        self.generate_id_2 = PhotoImage(
            file=relative_to_assets("generate_id_2.png"))
        
          
        def generate_id_bttn(img1, img2):
            mybtn1 = Button(self.left_bar, border=0, cursor='hand2', bg="#152364", activebackground="#152364",relief=SUNKEN)
            image_a = img1
            image_b = img2

            def on_enter(e):
                mybtn1['image'] = image_b

            def on_leave(e):
                mybtn1['image'] = image_a

            mybtn1.image_normal = image_a
            mybtn1.image_hover = image_b
            mybtn1['image'] = mybtn1.image_normal
            # Initially show the hover image            
            mybtn1.bind("<Enter>", on_enter)
            mybtn1.bind("<Leave>", on_leave)
            mybtn1.place(x=18, y=465)
            mybtn1.config(command=self.generate_id_card,
            relief="flat"
        )
        
        
        generate_id_bttn(self.generate_id_1, self.generate_id_2)
       #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
          
        self.modify_group_1 = PhotoImage(
            file=relative_to_assets("modify_1.png"))
        self.modify_group_2 = PhotoImage(
            file=relative_to_assets("modify_2.png"))
        
          
        def modify_bttn(img1, img2):
            mybtn1 = Button(self.left_bar, border=0, cursor='hand2', bg="#152364", activebackground="#152364",relief=SUNKEN)
            image_a = img1
            image_b = img2

            def on_enter(e):
                mybtn1['image'] = image_b

            def on_leave(e):
                mybtn1['image'] = image_a

            mybtn1.image_normal = image_a
            mybtn1.image_hover = image_b
            mybtn1['image'] = mybtn1.image_normal
            # Initially show the hover image            
            mybtn1.bind("<Enter>", on_enter)
            mybtn1.bind("<Leave>", on_leave)
            mybtn1.place(x=18, y=385)
            mybtn1.config(command=lambda:print("Under Development"),
            relief="flat"
        )
        
        
        modify_bttn(self.modify_group_1, self.modify_group_2)
       #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        self.excel_group_1 = PhotoImage(
            file=relative_to_assets("excel_1.png"))
        self.excel_group_2 = PhotoImage(
            file=relative_to_assets("excel_2.png"))
        
          
        def excel_bttn(img1, img2):
            mybtn1 = Button(self.left_bar, border=0, cursor='hand2', bg="#152364", activebackground="#152364",relief=SUNKEN)
            image_a = img1
            image_b = img2

            def on_enter(e):
                mybtn1['image'] = image_b

            def on_leave(e):
                mybtn1['image'] = image_a

            mybtn1.image_normal = image_a
            mybtn1.image_hover = image_b
            mybtn1['image'] = mybtn1.image_normal
            # Initially show the hover image            
            mybtn1.bind("<Enter>", on_enter)
            mybtn1.bind("<Leave>", on_leave)
            mybtn1.place(x=18, y=545)
            mybtn1.config(command=self.export_to_excel,
            relief="flat"
        )
        
        
        excel_bttn(self.excel_group_1, self.excel_group_2)
        
        self.exit_group_1 = PhotoImage(
            file=relative_to_assets("exit_1.png"))
        self.exit_group_2 = PhotoImage(
            file=relative_to_assets("exit_2.png"))
        
        
        def exit_bttn(img1, img2):
            mybtn1 = Button(self.left_bar, border=0, cursor='hand2', bg="#152364", activebackground="#152364",relief=SUNKEN)
            image_a = img1
            image_b = img2

            def on_enter(e):
                mybtn1['image'] = image_b

            def on_leave(e):
                mybtn1['image'] = image_a

            mybtn1.image_normal = image_a
            mybtn1.image_hover = image_b
            mybtn1['image'] = mybtn1.image_normal
            # Initially show the hover image            
            mybtn1.bind("<Enter>", on_enter)
            mybtn1.bind("<Leave>", on_leave)
            mybtn1.place(x=18, y=685)
            mybtn1.config(command=lambda:self.root.destroy(),
            relief="flat"
        )
        
        
        exit_bttn(self.exit_group_1, self.exit_group_2)
    
        
            
        self.doc_image_1 = PhotoImage(
            file=relative_to_assets("doc_icon_1.png"))
        self.doc_image_2 = PhotoImage(
            file=relative_to_assets("doc_icon_2.png"))
       
        self.frame_image = PhotoImage(
            file=relative_to_assets("frame_image.png"))
    
        self.submit_image_2 = PhotoImage(
            file=relative_to_assets("submit.png"))
        self.back_image_2 = PhotoImage(
            file=relative_to_assets("back.png"))
        self.photo_image = PhotoImage(
            file=relative_to_assets("button_6.png"))
        self.save_photo_2 = PhotoImage(
            file=relative_to_assets("Save_button_2.png"))
        
        
        
       

                
        # Treeview in Middle Frame
        self.tree = ttk.Treeview(self.database_frame, columns=("Name", "Year"))
        self.tree.column('#0', width=80)
        self.tree.column('Name', width=250)
        self.tree.column('Year', width=185)
        self.tree.heading("#0", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Year", text="Department & Year")
        self.tree.bind("<ButtonRelease-1>", self.on_select)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_select)
        self.tree.pack(fill="both", expand=True)
        style = ttk.Style()
        style.configure("Treeview", font=("Comic Sans MS", 11), background="#FFFFFF", fieldbackground="#FFFFFF", foreground="black", selectbackground="#333333", selectforeground="white", rowheight=65)
        style.map("Treeview", background=[("selected", "#5abbf0")])
        style.configure("Treeview.Heading", font=("Comic Sans MS", 14))
        self.displayed_student_details = tk.Canvas(self.details_frame,width=685, height=750,bg="#FFFFFF")
        self.displayed_student_details.pack(fill="both", expand=True)
    

        self.load_students()
    def delete_selected_student(self):
        # Get the selected student
        selected_item = self.tree.focus()

        if selected_item:  # Check if any item is selected
            # Get the student's ID
            student_id = self.tree.item(selected_item)['text']

            # Delete the student from the database
            self.db.delete_student(student_id)

            # Update the Treeview to reflect the changes
            self.load_students()
        else:
            messagebox.showerror("Error", "Select a student first")

    def add_student(self):
        self.middle_frame.destroy()
        self.left_frame.destroy()
        
        self.canvas1 = Canvas(
            self.root_canvas,
            bg = "#FCF8EE",
            height = 900,
            width = 1500,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas1.place(x = 0, y = 0)

        
      
        self.image_left_image = PhotoImage(
            file=relative_to_assets("image_1_1.png"))
        self.left_image = self.canvas1.create_image(
            725.0,
            430.0,
            image=self.image_left_image
        )
        '''self.image_boy_image = PhotoImage(
            file=relative_to_assets("image_4.png"))
        self.boy_image = self.canvas1.create_image(
            540.0,
            170.0,
            image=self.image_boy_image
        )

        self.image_girl_image= PhotoImage(
            file=relative_to_assets("image_5.png"))
        self.girl_image = self.canvas1.create_image(
            595.0,
            464.0,
            image=self.image_girl_image
        )'''
        

       
        def back_to_main():
            self.canvas1.destroy()
            self.root_canvas.destroy()
            StudentApp(root)
            root.mainloop()
        # Function to add the student details to the database
        
        def add_to_database():
            roll_no = roll_no_var.get()
            name = name_var.get()
            gender = gender_var.get()
            dob = dob_var.get()
            address = address_var.get()
            phone_no = phone_no_var.get()
            email = email_var.get()
            dept = dept_var.get()
            year = year_var.get()
            identity_proof = identity_proof_var.get()
            last_qualification=last_qualification_var.get()
            image_data=None
            qualification_cert_data=None
            identity_proof_image_data=None
            
                            
            if roll_no and name:
                if image_path:
                    with open(image_path, "rb") as f:
                        image_data = f.read()
                if qualification_cert_path:
                    try:
                        with open(qualification_cert_path, "rb") as f:
                            qualification_cert_data = f.read()
                    except Exception as e:
                        print("Error reading class 10 mark sheet:", e)

                # Read and save identity_proof image
                if identity_proof_image_path:
                    try:
                        with open(identity_proof_image_path, "rb") as f:
                            identity_proof_image_data = f.read()
                    except Exception as e:
                        print("Error reading identity_proof image:", e)
                        
                    self.db.insert_student(roll_no, name, image_data, gender, dob, address, phone_no, email, dept, year, identity_proof,last_qualification,qualification_cert_data,identity_proof_image_data)
                    #self.load_students()
                    self.canvas1.destroy()
                    self.root_canvas.destroy()
                 
                    #StudentApp(root)
                    #root = tk.Tk()
                    StudentApp(root)
                    root.mainloop()

                    
                else:
                    messagebox.showerror("Error", "Please select an image.")
            else:
                messagebox.showerror("Error", "Please enter Roll No and Name.")

       
       # Define variables for storing input data
        roll_no_var = tk.StringVar()
        name_var = tk.StringVar()
        gender_var = tk.StringVar()
        dob_var = tk.StringVar()
        address_var = tk.StringVar()
        phone_no_var = tk.StringVar()
        email_var = tk.StringVar()
        dept_var = tk.StringVar()
        year_var = tk.StringVar()
        identity_proof_var = tk.StringVar()
        image_path = ""
        last_qualification_var = tk.StringVar()
        qualification_cert_path= ""
        identity_proof_image_path= ""
        
        def identity_proof_image():
            nonlocal identity_proof_image_path
            identity_proof_image_path = filedialog.askopenfilename(defaultextension=".jpeg", filetypes=[("JPEG files", "*.jpg;*.jpeg")], title="Select Your identity_proof Card")
            if identity_proof_image_path:
                messagebox.showinfo("Message", "Your identity_proof Card Uploaded.......")


      
                                
        def select_image():
            nonlocal image_path
            image_path = filedialog.askopenfilename(defaultextension=".jpeg", filetypes=[("JPEG files", "*.jpg;*.jpeg")], title="Select Your Passport Image")
            if image_path:
                try:
                    image = Image.open(image_path)
            
                    # Resize the image to fit within a 200 x 250 box while maintaining aspect ratio
                    image.thumbnail((200, 250), Image.LANCZOS)
                    
                    # Create a blank white background image with size 200 x 250
                    new_image = Image.new("RGB", (200, 250), "white")
                    
                    # Calculate the position to center the resized image on the white background
                    left = (200 - image.width) // 2
                    top = (250 - image.height) // 2
                    
                    # Paste the resized image onto the white background
                    new_image.paste(image, (left, top))
                    
                    # Convert the resized image to Tkinter PhotoImage format
                    photo_image = ImageTk.PhotoImage(new_image)
                    
                    # Display the resized image on the photo_label
                    photo_label.configure(image=photo_image)
                    photo_label.image = photo_image  # Keep a reference to prevent garbage collection
                    
                    messagebox.showinfo("Message", "Your Photo Uploaded.......")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                                
        def qualification_cert_image():
            nonlocal qualification_cert_path
            qualification_cert_path= filedialog.askopenfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Select Your Marksheet")
            if qualification_cert_path:
                messagebox.showinfo("Message", "Your Class 10 Marksheet Uploaded.......")
                
        
       


        
        roll = Entry(
            self.canvas1,
            textvariable=roll_no_var,
            font=("Comic Sans MS", 14,"bold"),
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0
        )
        roll.place(
            x=190.0,
            y=300.0,
            width=252.0,
            height=25.0
        )
        
        

        
        name = Entry(
            self.canvas1,
            textvariable=name_var,
            font=("Comic Sans MS", 14,"bold"),
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0
        )
        name.place(
            x=190.0,
            y=58.0,
            width=252.0,
            height=25.0
        )
        
       

        photo_label = Label(
                    self.canvas1,
                    #width=13,
                    #height=7,
                    bg="#FCF8EE",
                    bd=1,
                    relief="solid")
        photo_label.place(
                    x=460.0,
                    y=58.0,
                    width=180.0,
                    height=220.0)


        
        photo = Button(
            self.canvas1,
            image=self.photo_image ,
            borderwidth=0,
            bg="#FCF8EE",
            highlightthickness=0,
            activebackground="white",
            command=select_image,
            relief="flat"
        )
        photo.place(
            x=484.0,
            y=279.0,
            width=45.0,
            height=45.0
        )


        male_icon = "\u2642"
        female_icon = "\u2640"
        transgender_icon = "\u26A7"
        def select_male():
            gender_var.set("Male")
            #messagebox.showwarning("Caution", f"Selected gender: {gender_var.get()}")
            male.config(bg="#316bff", fg="white")
            female.config(bg="#FCF8EE", fg="#000716")
            transgender.config(bg="#FCF8EE", fg="#000716")

        def select_female():
            gender_var.set("Female")
            #messagebox.showwarning("Caution", f"Selected gender: {gender_var.get()}")
            male.config(bg="#316bff", fg="white")
            female.config(bg="#316bff", fg="white")
            male.config(bg="#FCF8EE", fg="#000716")
            transgender.config(bg="#FCF8EE", fg="#000716")

        def select_transgender():
            gender_var.set("Transgender")
            #messagebox.showwarning("Caution", f"Selected gender: {gender_var.get()}")
            transgender.config(bg="#316bff", fg="white")
            male.config(bg="#FCF8EE", fg="#000716")
            female.config(bg="#FCF8EE", fg="#000716")

        male = Button(
            self.canvas1,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            font=("Comic Sans MS", 10,"bold"),
            text=f"Male {male_icon}",
            activebackground="#316bff",
            activeforeground="white",
            highlightthickness=0,
            command=select_male,
            relief="solid"
        )
        male.place(
            x=190.0,
            y=102.0,
            width=70.0,
            height=25.0
        )
        female = Button(
            self.canvas1,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            highlightthickness=0,
            font=("Comic Sans MS", 10,"bold"),
            text=f"Female {female_icon}",
            activebackground="#316bff",
            activeforeground="white",
            command=select_female,
            relief="solid"
        )
        female.place(
            x=280.0,
            y=102.0,
            width=70.0,
            height=25.0
        )

        transgender = Button(
            self.canvas1,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            highlightthickness=0,
            font=("Comic Sans MS", 10,"bold"),
            activebackground="#316bff",
            activeforeground="white",
            text=f"Trans {transgender_icon}",
            command=select_transgender,
            relief="solid"
        )
        transgender.place(
            x=370.0,
            y=102.0,
            width=70.0,
            height=25.0
        )
        
        
        def select_date(top, cal):
            selected_date = cal.selection_get()
            dob_var.set(selected_date)
            self.date_of_birth.config(text=selected_date.strftime("%Y-%m-%d"))
            top.destroy()
        
        # Function to open calendar window
        def open_calendar():
            top = tk.Toplevel()
            cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
            cal.pack(fill="both", expand=True)
            ok_button = tk.Button(top, text="OK", command=lambda: select_date(top, cal))
            ok_button.pack()
        
               
        self.dob_calender_image = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.dob_calender = Button(
            self.canvas1,
            image=self.dob_calender_image,
            borderwidth=0,
            highlightthickness=0,
            bg="#FCF8EE",
            activebackground="white",
            command=open_calendar,
            relief="flat"
        )
        self.dob_calender.place(
            x=190.0,
            y=150.0,
            width=30.0,
            height=33.0
        )


        self.date_of_birth =  Label(
            self.canvas1,
            bd=0,
            #text=f" {dob_var.get()}",
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0,
            font=("Comic Sans MS", 14, "bold")
        )
        self.date_of_birth.place(
            x=240.0,
            y=155.0,
            width=200.0,
            height=25.0
        )

      
            
        year_options = ["First  Year", "Second  Year", "Third  Year", "Fourth  Year"]
        
        year_combobox = Combobox(
                        self.canvas1,
                        textvariable=year_var,
                        values=year_options,
                        font=("Comic Sans MS", 10,"bold"),
                        #command=select_year
                        state="readonly"
                         )
        #year_combobox.config(font=("Comic Sans MS", 10))
       
        year_combobox.place(
            x=190.0,
            y=197.0,
            width=252.0,
            height=25.0
        )
     
        
        department_options = ["Computer Science  &  Engineering","Mechanical Engineering","Civil Engineering","Electrical Engineering","Electronic &  Communication Engineering"]
        department_combobox = Combobox(
                        self.canvas1,
                        textvariable=dept_var,
                        values=department_options,
                        font=("Comic Sans MS", 10,"bold"),
                        state="readonly"
                        )
        #department_combobox.config(font=('Helvetica', 10))
        department_combobox.place(
            x=190.0,
            y=248.0,
            width=252.0,
            height=25.0
        )
        
        height_var = StringVar()
        person_height = Entry(
            self.canvas1,
            textvariable=height_var,
            font=("Comic Sans MS", 14,"bold"),
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0
        )
        person_height.place(
            x=190.0,
            y=345.0,
            width=145.0,
            height=25.0
        )
        
        weight_var = StringVar()
        person_weight = Entry(
            self.canvas1,
            textvariable=height_var,
            font=("Comic Sans MS", 14,"bold"),
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0
        )
        person_weight.place(
            x=440.0,
            y=345.0,
            width=120.0,
            height=27.0
        )
        
        
        sp_abled_options = ["Yes","No"]
        sp_abled_var = StringVar()
        sp_abled_combobox = Combobox(
                        self.canvas1,
                        textvariable=sp_abled_var,
                        values=sp_abled_options,
                        state="readonly")
        sp_abled_combobox.config(font=("Comic Sans MS", 10,"bold"))

        sp_abled_combobox.place(
            x=440.0,
            y=392.0,
            width=120.0,
            height=25.0
        )
        

        self.sp_abled_image = PhotoImage(
            file=relative_to_assets("button_8.png"))
        sp_abled_image_proof = Button(
            self.canvas1,
            image=self.sp_abled_image,
            bg="#FCF8EE",
            activebackground="white",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("Specially Abled"),
            relief="flat"
        )
        sp_abled_image_proof.place(
            x=580.0,
            y=347.0,
            width=59.0,
            height=44.0
        )
        
        blood_group_options = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
        blood_group_var = StringVar()
        blood_group_combobox = Combobox(
                        self.canvas1,
                        textvariable=blood_group_var,
                        values=blood_group_options,
                        state="readonly")
        blood_group_combobox.config(font=("Comic Sans MS", 10,"bold"))
        blood_group_combobox.place(
            x=190.0,
            y=392.0,
            width=145.0,
            height=25.0
        )
        
        
        
        isd_countries = {
            "+91": "India",
            "+1": "United States",
            
        }
        isd_options = [f"{isd} - {country}" for isd, country in isd_countries.items()]



        def on_focus_out(event):
            if ph_no.get() != "" and isd_var.get() !="":
                phone_no_var.set(isd_var.get()+ph_no.get())
                print("Custom option entered:", phone_no_var.get())
      
        def show_isd_code(event):
            selected_option = isd_var.get()
            if selected_option:
                isd_code = selected_option.split()[0]  # Extracting ISD code
                isd_var.set(isd_code)  # Set isd_var to ISD code
                print("ISD Var Value:", isd_var.get())  # Print the value of isd_var

        #isd_options = ["FIRST", "SECOND", "TRD", "FOURTH"]
        isd_var = StringVar()
        isd_var.set("")
        ph_no = StringVar()
        isd_combobox = Combobox(
                        self.canvas1,
                        textvariable=isd_var,
                        values=isd_options,
                        state="readonly")
        isd_combobox.config(font=("Comic Sans MS", 10,"bold"))
        isd_combobox.bind("<<ComboboxSelected>>", show_isd_code) 
        isd_combobox.place(
            x=120.0,
            y=485.0,
            width=170.0,
            height=25.0
        )

        phone_no = Entry(
            self.canvas1,
            textvariable=ph_no ,
            font=("Comic Sans MS", 14,"bold"),
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0
        )
        phone_no.place(
            x=300.0,
            y=485.0,
            width=340.0,
            height=25.0
        )
        
        phone_no.bind("<FocusOut>", on_focus_out)

        def on_focus_out2(event):
            if email_add.get() != "" and email_domain_var.get() != "":
                email_var.set(email_add.get()+email_domain_var.get())
                print("Custom option :", email_var.get())
        email_add = StringVar()
        email_domain_var = StringVar()
        email_domain_var.set("")
        email_username = Entry(
            self.canvas1,
            textvariable=email_add ,
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            font=("Comic Sans MS", 14,"bold"),
            relief="solid",
            highlightthickness=0
        )
        email_username.place(
            x=120.0,
            y=555.0,
            width=350.0,
            height=25.0
        )
        email_username.bind("<FocusOut>", on_focus_out2)

        def on_select(event):
            selected_option = email_domain_var.get()
            if selected_option == "Custom":
                email_domain_combobox.config(state="normal")
                email_domain_combobox.delete(0, "end")
                email_domain_combobox.focus_set()
                #email_domain_combobox.on_focus_out3()
            else:
                email_domain_combobox.config(state="readonly")

        def on_focus_out3(event):
            if email_domain_var.get() != "":
                print("Custom option entered:", email_domain_var.get())
                on_focus_out2(event)


        #email_domain_options = ["Custom", "FIRST", "SOND", "THIRD", "FOURTH"]
        email_domain_options = [
            "Custom","@gmail.com", "@yahoo.com", "@outlook.com", "@rediffmail.com", 
            "@hotmail.com", "@microsoft.com"]

        
        email_domain_combobox = Combobox(
            self.canvas1,
            textvariable=email_domain_var,
            values=email_domain_options,
            state="readonly"
        )
        email_domain_combobox.config(font=("Comic Sans MS", 10,"bold"))
        email_domain_combobox.place(
            x=480.0,
            y=555.0,
            width=160.0,
            height=26.0
        )

        email_domain_combobox.bind("<<ComboboxSelected>>", on_select)
        email_domain_combobox.bind("<FocusOut>", on_focus_out3)
    
        
        all_countries = {
            "🇮🇳": "India",
            "🇦🇩": "Andorra",
           }

        # Create a list of ISD codes and country names in the format "ISD Code - Country Name"
        nationality_options = [f"{flag} - {country}" for flag, country in all_countries.items()]

        def show_country(event):
            selected_option = nationality_var.get()
            if selected_option:
                country_name = ' '.join(selected_option.split()[2:]) # Extracting ISD code
                nationality_var.set(country_name)  # Set isd_var to ISD code
                print("Contry:", nationality_var.get())  # Print the value of isd_var


        nationality_var = StringVar()
        nationality_combobox = Combobox(
                        self.canvas1,
                        textvariable=nationality_var,
                        values=nationality_options,
                        state="readonly")
        nationality_combobox.config(font=("Comic Sans MS", 10,"bold"))
        nationality_combobox.bind("<<ComboboxSelected>>", show_country) 
        nationality_combobox.place(
            x=145.0,
            y=626.0,
            width=240.0,
            height=25.0
        )


        religion_options = ["Hinduism","Christianity","Islam","Buddhism","Judaism","Sikhism","Jainism"]
        religion_var = StringVar()
        religion_combobox = Combobox(
                        self.canvas1,
                        textvariable=religion_var,
                        values=religion_options,
                        state="readonly")
        religion_combobox.config(font=("Comic Sans MS", 10))

        religion_combobox.place(
            x=470.0,
            y=626.0,
            width=170.0,
            height=25.0
        )
        
        
        address = Entry(
            self.canvas1,
            textvariable=address_var,
            font=("Comic Sans MS", 16,"bold"),
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0
        )

        address.place(
            x=145.0,
            y=670.0,
            width=495.0,
            height=25.0
        )
        
        def on_focus_out_id(event):
            if id_no_var.get() != "" and id_category_var.get() !="":
                identity_proof_var.set(id_category_var.get()+" No is -"+id_no_var.get())
                print("ID IS: ",identity_proof_var.get())
      
        def show_id_catg(event):
            selected_option = id_category_var.get()
            if selected_option:
                print("CATG:", id_category_var.get())  # Print the value of isd_var

       
       
        id_category_options = ["Aadhaar", "Passport","Driving License", "PAN Card",
                               "Voter ID Card","Post Office ID card","Bank Account Passbook",
                               "Other Photo ID  by Govt."]
        id_no_var=StringVar()
        id_category_var = StringVar()
        id_category_var.set("")
        id_no_var.set("")
        id_category_combobox = Combobox(
                        self.canvas1,
                        textvariable=id_category_var ,
                        values=id_category_options,
                        state="readonly")
        id_category_combobox.config(font=("Comic Sans MS", 10,"bold"))


        id_category_combobox.place(
            x=820.0,
            y=77.0,
            width=240.0,
            height=25.0
        )
        
        id_category_combobox.bind("<<ComboboxSelected>>", show_id_catg) 
        
        
        
        id_no = Entry(
            self.canvas1,
            textvariable=id_no_var,
            font=("Comic Sans MS", 16,"bold"),
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0
        )
        id_no.place(
            x=1075.0,
            y=77.0,
            width=308.0,
            height=25.0
        )
        
        id_no.bind("<FocusOut>", on_focus_out_id)
        
        self.identity_image = PhotoImage(
            file=relative_to_assets("button_7.png"))
        identity_doc = Button(
            self.canvas1,
            image=self.identity_image,
            borderwidth=0,
            bg="#FCF8EE",
            highlightthickness=0,
            activebackground="white",
            command=identity_proof_image,
            relief="flat"
        )
        identity_doc .place(
            x=1315.0,
            y=110.0,
            width=70.0,
            height=120.0
        )
                      
                
        def on_select_degree(event):
            selected_option = degree_name_var.get()
            if selected_option == "Others":
                degree_name_combobox.config(state="normal")
                degree_name_combobox.delete(0, "end")
                degree_name_combobox.focus_set()
            else:
                degree_name_combobox.config(state="readonly")

        def on_focus_out_degree(event):
            if degree_name_var.get() != "" and degree_marks.get() != "" and degree_year.get() != "":
                last_qualification_var.set(degree_name_var.get() + ",with " + degree_marks.get()+" % marks, in " + degree_year.get())
                print("Degree :", last_qualification_var.get())


        degree_name_options = ["Others","Higher Secondary ", "Polytechnic","B.Sc (CS/IT)", "B.Sc(Others)", "B.C.A"]
        degree_marks = StringVar()
        degree_name_var = StringVar()
        degree_year = StringVar()
        degree_year.set("")
        degree_name_var.set("")
        degree_marks.set("")
        degree_name_combobox = Combobox(
            self.canvas1,
            textvariable=degree_name_var,
            values=degree_name_options,
            state="readonly"
        )
        degree_name_combobox.config(font=("Comic Sans MS", 10,"bold"))
        degree_name_combobox.place(
            x=930.0,
            y=320.0,
            width=382.0,
            height=25.0
        )
        
        
        degree_percentage = Entry(
            self.canvas1,
            textvariable=degree_marks,
            font=("Comic Sans MS", 14,"bold"),
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0
        )
        degree_percentage.place(
            x=930.0,
            y=375.0,
            width=150.0,
            height=25.0
        )


        degree_year = Entry(
            self.canvas1,
            textvariable=degree_year,
            font=("Comic Sans MS", 14,"bold"),
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0
        )
        degree_year.place(
            x=1160.0,
            y=375.0,
            width=150.0,
            height=25.0
        )
        
        degree_name_combobox.bind("<<ComboboxSelected>>", on_select_degree)
        degree_name_combobox.bind("<FocusOut>", on_focus_out_degree)
        degree_year.bind("<FocusOut>", on_focus_out_degree)
        degree_percentage.bind("<FocusOut>", on_focus_out_degree)
        
        
        self.pr_degree_image = PhotoImage(
            file=relative_to_assets("button_8.png"))
        pr_degree = Button(
            self.canvas1,
            image=self.pr_degree_image,
            borderwidth=0,
            bg="#FCF8EE",
            highlightthickness=0,
            activebackground="white",
            command=qualification_cert_image,
            relief="flat"
        )
        pr_degree.place(
            x=1320.0,
            y=315.0,
            width=70.0,
            height=53.0
        )
        
        def on_select_gr_name(event):
            selected_option = title_var.get()
            '''if selected_option == "Others":
                degree_name_combobox.config(state="normal")
                degree_name_combobox.delete(0, "end")
                degree_name_combobox.focus_set()
            else:
                degree_name_combobox.config(state="readonly")'''

        def on_focus_out_gr_name(event):
            if title_var.get() != "" and care_of_name.get() != "":
                gurdian_name.set(title_var.get() + "  " + care_of_name.get())
                print("Degree :", gurdian_name.get())
                
              
        title_var = StringVar()
        care_of_name = StringVar()
        gurdian_name = StringVar()
        
        gurdian_name.set("")
        title_var.set("")
        care_of_name.set("")
        
        title_options = ["Mr.","Mrs."]
        tiltle_combobox = Combobox(
            self.canvas1,
            textvariable=title_var,
            values=title_options,
            state="readonly"
        )
        tiltle_combobox.config(font=("Comic Sans MS", 10,"bold"))
        tiltle_combobox.place(
            x=820.0,
            y=492.0,
            width=80.0,
            height=25.0
        )
                
        care_of = Entry(
            self.canvas1,
            textvariable=care_of_name,
            font=("Comic Sans MS", 16,"bold"),
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0
        )

        care_of.place(
            x=930.0,
            y=492.0,
            width=260.0,
            height=25.0
        )
       
        
        tiltle_combobox.bind("<<ComboboxSelected>>", on_select_gr_name)
        tiltle_combobox.bind("<FocusOut>", on_focus_out_gr_name)
        care_of.bind("<FocusOut>", on_focus_out_gr_name)
                 
        emergency_var=StringVar()
        emergency = Entry(
            self.canvas1,
            textvariable=emergency_var,
            font=("Comic Sans MS", 16,"bold"),
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0
        )

        emergency.place(
            x=915.0,
            y=538.0,
            width=460.0,
            height=80.0
        )
        
       
        
        games_var=StringVar()
        games = Entry(
            self.canvas1,
            textvariable=games_var,
            font=("Comic Sans MS", 16,"bold"),
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0
        )

        games.place(
            x=915.0,
            y=658.0,
            width=220.0,
            height=25.0
        )
        skills_var=StringVar()
        skills = Entry(
            self.canvas1,
            textvariable=skills_var,
            font=("Comic Sans MS", 16),
            bd=0,
            bg="#FCF8EE",
            fg="#000716",
            borderwidth=1,
            relief="solid",
            highlightthickness=0
        )

        skills.place(
            x=1202.0,
            y=658.0,
            width=170.0,
            height=25.0
        )
        
        
        submit_2 = Button(
            self.canvas1,
            image=self.submit_image_2,
            borderwidth=0,
            highlightthickness=0,
            bg="#FCF8EE",
            command=add_to_database,
            relief="flat"
        )
        submit_2.place(
            x=826.0,
            y=704.0,
            width=550.0,
            height=30.0
        )
        
        back_2 = Button(
            self.canvas1,
            image=self.back_image_2,
            borderwidth=0,
            highlightthickness=0,
            bg="#FCF8EE",
            command=back_to_main,
            relief="flat"
        )
        back_2.place(
            x=82.0,
            y=704.0,
            width=550.0,
            height=30.0
        )
 
 
      
    def load_students(self):
        self.tree.delete(*self.tree.get_children())
        students = self.db.fetch_students()
        #print(student[5])
        for student in students:
            student_id = student[0]
            value=student[6]
            if value == "Computer Science  &  Engineering" or "CSE":
                value="CSE"
            elif value == "Mechanical Engineering" or "ME":
                value="ME"
            elif value == "Civil Engineering" or "CE":
                value="CE"
            elif value == "Electrical Engineering" or "EE":
                value="EE"
            elif value == "Electronic &  Communication Engineering" or "ECE":
                value="ECE"
            else:
                pass 
            self.tree.insert("", "end", text=student_id, values=(student[2], (value+"  -  "+student[5])))
            

    def on_select(self, event):
        if not self.tree.selection():
            messagebox.showwarning("Caution", "Please select a student first.")
            return
        
        selected_item = self.tree.selection()[0]
        student_id = self.tree.item(selected_item, "text")
        self.display_student_details(student_id)
  

    def display_student_details(self, student_id):
        self.displayed_student_details.destroy()
        self.displayed_student_details = tk.Canvas(self.details_frame,width=685, height=700,bg="#F8FCFC")
       
        self.displayed_student_details.pack(fill="both", expand="True")
        frame_image = self.displayed_student_details.create_image(
            340.0,
            442.0,
            image=self.frame_image
        )
        #self.displayed_student_details.delete("all")
      
        image_data = self.db.get_image(student_id)
        qualification_cert_data = self.db.get_qualification_cert(student_id)
        identity_proof_image_data = self.db.get_identity_proof_image(student_id)
        if image_data:
            img = Image.open(io.BytesIO(image_data))
            img = img.resize((150, 150), Image.LANCZOS)

            # Create circular mask
            mask = Image.new("L", (img.width, img.height), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, img.width, img.height), fill=255)

            img.putalpha(mask)

            photo = ImageTk.PhotoImage(img)
            #label = tk.Label(self.displayed_student_details, image=photo, bg="white", fg="black")
            #label.image = photo
            #label.place(x=285, y=7)  # Adjust coordinates as needed
        
            
        def save_image_bttn(img1, img2):
            mybtn = Button(self.displayed_student_details, border=0, cursor='hand2', bg="white", activebackground="white",relief=SUNKEN)
            image_a = img1
            image_b = img2

            def on_enter(e):
                mybtn['image'] = image_b

            def on_leave(e):
                mybtn['image'] = image_a

            mybtn.image_normal = image_a
            mybtn.image_hover = image_b
            mybtn['image'] = mybtn.image_normal
            # Initially show the hover image
            
            mybtn.bind("<Enter>", on_enter)
            mybtn.bind("<Leave>", on_leave)
            mybtn.place(x=285, y=7)
            mybtn.config(command=lambda: self.save_image(image_data))

    
        save_image_bttn(photo, self.save_photo_2 )
        
        #Button(self.displayed_student_details, image=photo,bg="white",activebackground="white", command=lambda: self.save_image(image_data),bd=0).place(x=285.0, y=7.0)

        student_details = self.db.cur.execute("SELECT roll_no,name, gender, dob, address, phone_no, email, dept, year, identity_proof,last_qualification FROM students WHERE id=?", (student_id,)).fetchone()

        if student_details:
            custom_font = "Comic Sans MS", 13
            custom_font2 = "Comic Sans MS", 14
            custom_font3 = "Comic Sans MS", 12

            # Place each label and its corresponding data individually
            #roll_no
            tk.Label(self.displayed_student_details, text=f"{student_details[0]}", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=100, y=219)
            #name
            tk.Label(self.displayed_student_details, text=f"{student_details[1]}", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=90, y=187)
            #gender
            tk.Label(self.displayed_student_details, text=f"{student_details[2]}", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=570, y=219)
            #dob
            tk.Label(self.displayed_student_details, text=f" {student_details[3]}", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=360, y=219)
            #phone_no
            tk.Label(self.displayed_student_details, text=f"{student_details[5]}", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=115, y=250)
            #email
            tk.Label(self.displayed_student_details, text=f"{student_details[6]}", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=340, y=250)
          
            
            #father & mother name 
            tk.Label(self.displayed_student_details, text="Mr._______", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=57, y=330)
            #identity proof   
            tk.Label(self.displayed_student_details, text=" Aadhar Card no.- "+f" {student_details[9]}", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=13, y=359)
            #nationality
            tk.Label(self.displayed_student_details, text=" Indian ",bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=130, y=387)
            #religion
            tk.Label(self.displayed_student_details, text=" Hindu ", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=460, y=387)
            #address
            tk.Label(self.displayed_student_details, text=f" {student_details[4]}",bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=95, y=420)
           
            # Button to save identity_proof image
            def save_address_proof_bttn(img1, img2):
                mybtn = Button(self.displayed_student_details, border=0, cursor='hand2', bg="white", activebackground="white",relief=SUNKEN)
                image_a = img1
                image_b = img2

                def on_enter(e):
                    mybtn['image'] = image_b

                def on_leave(e):
                    mybtn['image'] = image_a

                mybtn.image_normal = image_a
                mybtn.image_hover = image_b
                mybtn['image'] = mybtn.image_normal
                # Initially show the hover image
                
                mybtn.bind("<Enter>", on_enter)
                mybtn.bind("<Leave>", on_leave)
                mybtn.place(x=605, y=310)
                mybtn.config(command=lambda: self.save_identity_proof_image(identity_proof_image_data))

        
            save_address_proof_bttn(self.doc_image_1, self.doc_image_2)
                  
            #Button(self.displayed_student_details, image=self.doc_image_1, command=lambda: self.save_identity_proof_image(identity_proof_image_data),bd=0).place(x=255.0, y=342.0)
            
            
            #height
            tk.Label(self.displayed_student_details, text="____  cm", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=100, y=500)
            #weight
            tk.Label(self.displayed_student_details, text="____  kg", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=335, y=500)
            #blood group
            tk.Label(self.displayed_student_details, text=" B +", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=500, y=532)
            #specially abled
            tk.Label(self.displayed_student_details, text="No", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=175, y=530)
            #medical emergency
            tk.Label(self.displayed_student_details, text="12347891045", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=190, y=563)
            #to save specially abled proof doc
            
            
            # Button to save identity_proof image
            def save_medical_proof_bttn(img1, img2):
                mybtn = Button(self.displayed_student_details, border=0, cursor='hand2', bg="white", activebackground="white",relief=SUNKEN)
                image_a = img1
                image_b = img2

                def on_enter(e):
                    mybtn['image'] = image_b

                def on_leave(e):
                    mybtn['image'] = image_a

                mybtn.image_normal = image_a
                mybtn.image_hover = image_b
                mybtn['image'] = mybtn.image_normal
                # Initially show the hover image
                
                mybtn.bind("<Enter>", on_enter)
                mybtn.bind("<Leave>", on_leave)
                mybtn.place(x=605, y=474)
                mybtn.config(command=lambda: print("under Development"))

        
            save_medical_proof_bttn(self.doc_image_1, self.doc_image_2)
            
            
          
            #pervious degree
            tk.Label(self.displayed_student_details, text="I, did my Higher Secondary, with"+f" {student_details[10]}"+"  % marks, in 2020",bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=22, y=660)
            #games extra co-curriculam activity
            tk.Label(self.displayed_student_details, text="Games & Sports", bg="#F8FCFC", fg="#0BA5EC", font=custom_font).place(x=145, y=702)
            # Button to save previous mark sheet
            def save_degree_proof_bttn(img1, img2):
                mybtn = Button(self.displayed_student_details, border=0, cursor='hand2', bg="white", activebackground="white",relief=SUNKEN)
                image_a = img1
                image_b = img2

                def on_enter(e):
                    mybtn['image'] = image_b

                def on_leave(e):
                    mybtn['image'] = image_a

                mybtn.image_normal = image_a
                mybtn.image_hover = image_b
                mybtn['image'] = mybtn.image_normal
                # Initially show the hover image              
                mybtn.bind("<Enter>", on_enter)
                mybtn.bind("<Leave>", on_leave)
                mybtn.place(x=605, y=635)
                mybtn.config(command=lambda: self.save_qualification_cert(qualification_cert_data))       
            save_degree_proof_bttn(self.doc_image_1, self.doc_image_2)
    def save_image(self, image_data):
        filename = filedialog.asksaveasfilename(defaultextension=".jpeg", filetypes=[("JPEG files", "*.jpg;*.jpeg")], title="Save Your Image As")
        if filename:
            with open(filename, "wb") as f:
                f.write(image_data)

    def save_qualification_cert(self, qualification_cert_data):
        filename1 = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Save Your Marksheet As")
        if filename1:
            with open(filename1, "wb") as f2:
                f2.write(qualification_cert_data)

    def save_identity_proof_image(self,identity_proof_image_data):
        filename3 = filedialog.asksaveasfilename(defaultextension=".jpeg",filetypes=[("JPEG files", "*.jpg;*.jpeg")], title="Save Your identity_proof Crad As")
        if filename3:
            with open(filename3, "wb") as f4:
                f4.write(identity_proof_image_data)


    def generate_id_card(self):
        if not self.tree.selection():
            messagebox.showerror("Error", "Please select a student.")
            return
    
        
        selected_item = self.tree.selection()[0]
        student_id = self.tree.item(selected_item, "text")
        student_details = self.db.cur.execute("SELECT id,roll_no, name, image, gender, dob, address, phone_no, email, dept, year, identity_proof FROM students WHERE id=?", (student_id,)).fetchone()
        
        if student_details:
            od,roll_no, name, image_data, gender, dob, address, phone_no, email, dept, year, identity_proof = student_details
            
            background = Image.open(r"assets/frame0/background_image.jpg")
            background = background.resize((500, 850))  # Resize to match ID card size
            
            # Create blank ID card image
            id_card = Image.new('RGB', (500, 850), (255, 255, 255))
            
            # Paste background onto ID card
            id_card.paste(background, (0, 0))
            draw = ImageDraw.Draw(id_card)
            name_font = ImageFont.truetype("arial.ttf", 38)
            dept_font = ImageFont.truetype("arial.ttf", 28)
            id_font = ImageFont.truetype("arial.ttf",37)
            other_font = ImageFont.truetype("arial.ttf",22)
            text_color = "black"
            text_color1 = "black"
            name_position = (50, 266)
            dept_position = (260, 385)
            roll_position = (264, 150)
            bl_gr_position = (260, 440)
            valid_position = (260, 488)
            #draw.text(text_position, f"Roll No: {roll_no}", fill=text_color, font=font)           
            draw.text(name_position,  f"{name}", fill=text_color , font=name_font, stroke_width=1,
            stroke_fill="black")
            draw.text(dept_position,  f"MIT | {dept} | 2K20", fill=text_color , font=dept_font,stroke_width=1,
            stroke_fill="black")
            draw.text(roll_position,f"{roll_no}", fill=text_color , font=id_font,stroke_width=1,
            stroke_fill="black")
            draw.text(bl_gr_position,f"Blood Gr.   : ", fill=text_color , font=other_font)
            draw.text(valid_position,f"Valid Upto  : ", fill=text_color , font=other_font)
            img = Image.open(io.BytesIO(image_data))
            img = img.resize((211, 248), Image.LANCZOS)
            id_card.paste(img, (28, 392)) 
            qr_data = f"Roll No: {roll_no}\nName: {name}\nDate of Birth:  {dob}\nGender:  {gender}\nAddress:  {address}\nPhone No:  {phone_no}\nEmail:  {email}\nYear:  {year}\nDepartment:  {dept}\n AAdhar No.:  {identity_proof}"
            #qr_data = "Your QR data here"
            background_color = '#363435'
            qr_color = 'white'
            qr = qrcode.QRCode()
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr = qr.make_image(fill_color=qr_color, back_color=background_color)
            qr = qr.resize((195,195))
            qr.save("qrcode.png")
            qr_img = Image.open("qrcode.png")
            id_card.paste(qr_img, (10, 656))
            filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")], title="Save ID Card As")
            if filename:
                id_card.save(filename)
                messagebox.showinfo("Info",f" Dear {name} your ID card generted and saved successfully.")
                os.remove("qrcode.png")
        
                

    
    def export_to_excel(self):
        students = self.db.fetch_data_excel()
        if students:
            wb = Workbook()
            ws = wb.active
            ws.append(["ID", "Roll No", "Name", "Gender", "DOB", "Address", "Phone No.", "Email", "Dept", "Year", "identity_proof"])
            for student in students:
                ws.append(student)
            filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], title="Save Excel File As")
            if filename:
                wb.save(filename)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()




