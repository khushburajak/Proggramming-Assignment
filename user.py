import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

with sqlite3.connect("userdb.db") as db:
    cursor = db.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY AUTOINCREMENT, username text NOT NULL, password text NOT NULL, email text NOT NULL, full_name text NOT NULL); """)


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (Register, Login, Dashboard):

            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(Register)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # label of frame Layout 2
        label = ttk.Label(self, text ="Register New User", width=50,font=("bold", 30)).place(x = 700,y = 60) 

        username = ttk.Label(self, text ="Username", width=50,font=("bold", 15)).place(x = 600,y = 150) 
        username_input_area = ttk.Entry(self, text ="", width=50)
        username_input_area.place(x = 750,y = 150)
        
        full_name = ttk.Label(self, text ="Full Name", width=50,font=("bold", 15)).place(x = 600, y = 200) 
        full_name_input_area = ttk.Entry(self, text ="", width=50)
        full_name_input_area.place(x = 750,y = 200)
        
        email = ttk.Label(self, text = "Email", width=50,font=("bold", 15)).place(x = 600, y = 250)
        email_input_area = ttk.Entry(self, text="", width = 50)
        email_input_area.place(x = 750,y = 250)

        password = ttk.Label(self, text = "Password", width=50,font=("bold", 15)).place(x = 600, y = 300)
        password_input_area = ttk.Entry(self, text="", width = 50)
        password_input_area.place(x = 750,y = 300)

        def register_user():
            registred = False
            username = username_input_area.get()
            fullname = full_name_input_area.get()
            email = email_input_area.get()
            password = password_input_area.get()

            if username and fullname and email and password:
                cursor.execute("INSERT INTO users(username, email, full_name, password)VALUES(?,?,?,?)",(username,email,fullname,password))
                db.commit()
                registred = True

            if registred == True:
                messagebox.showinfo("Success", f"User: {username} registred success")
                controller.show_frame(Login)
            else:
                messagebox.showinfo("Info", "User Register Failed. Note: All fields are required")

        submit_button = tk.Button(self,text = "Register", command=register_user, font=("bold", 18), width=10, height=1).place(x = 800, y = 400)

        already_acc = tk.Button(self, text="Already have account?", command=lambda : controller.show_frame(Login), width=50, border=0, fg='blue', font=("bold", 12, 'underline'))
        already_acc.place(x=635,y=450)



class Login(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        labl_0 = tk.Label(self, text="Login",width=50,font=("bold", 30)).place(x=300,y=60)  
        user_name = tk.Label(self, text = "Username", width=50,font=("bold", 15)).place(x = 300, y = 150)
        user_name_input_area = tk.Entry(self, width = 50)
        user_name_input_area.place(x = 750,y = 150)

        password = tk.Label(self, text = "Password", width=50,font=("bold", 15)).place(x = 300, y = 200)
        password_input_area = tk.Entry(self, width = 50)
        password_input_area.place(x = 750,y = 200)


        def login():
            username = user_name_input_area.get()
            password = password_input_area.get()
            if username and password:
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
                fetched_data = cursor.fetchall() 
                if fetched_data:
                    messagebox.showinfo("Success", "Login Success")
                    controller.show_frame(Dashboard)
                else:
                    messagebox.showinfo("Failed", "Invalid Login Credential")
            else:
                messagebox.showinfo("Empty Fields", "Please enter username and password")
                
            
        submit_button = tk.Button(self,text = "Login", font=("bold", 18), command=login, width=10, height=1).place(x = 800, y = 250)

        create_acc = tk.Button(self, text="Don't have account?", command = lambda : controller.show_frame(Register), border=0, width=50,fg="blue", font=("bold", 12, 'underline')).place(x=635,y=300)  


class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        labl_0 = tk.Label(self, text="Welcome to Dashboard",width=50,font=("bold", 30)).place(x=300,y=60)  

        logout = tk.Button(self,text = "Logout", font=("bold", 18), command=lambda : controller.show_frame(Login), width=10, height=1).place(x = 800, y = 250)


app = tkinterApp()

app.title("Login Register System")
width= app.winfo_screenwidth()
height= app.winfo_screenheight()

app.geometry("%dx%d" % (width, height))

app.mainloop()
