from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def password_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]

    random.shuffle(password_list)
    password = ''.join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    web_info = web_entry.get()
    email_info = email_entry.get()
    password_info = password_entry.get()

    if len(web_info) == 0 or len(password_info) == 0:
        messagebox.showerror(title='Error!', message='Please fill in properly')
        return
    is_ok = messagebox.askokcancel(title=web_info,
                                   message=f"Recheck the details:\n Email:{email_info}\n Password:{password_info}\nSave this info ?")

    new_data_dict = {
        web_info: {
            "email": email_info,
            "password": password_info
        }
    }
    if is_ok:
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
                data.update(new_data_dict)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data_dict, data_file, indent=4)
        else:
            with open('data.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)

        web_entry.delete(0, 'end')
        password_entry.delete(0, 'end')


# -----------------------------SEARCH PASSWORD ------------------------#
def search():
    web_info = web_entry.get()
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title='Error!', message='No file to search in !')
    else:
        try:
            value_to_show = data[web_info]
        except KeyError:
            messagebox.showerror(title='Error!', message='No entry present!')
        else:
            messagebox.showinfo(title='here is your data',
                                message=f"Website:{web_info} \n email:{value_to_show['email']} \n password:{value_to_show['password']}")


# ---------------------------- UI SETUP ------------------------------- #

windows = Tk()
windows.title("Password Manager")
windows.config(padx=50, pady=50, bg='white')

canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
photo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=photo)
canvas.grid(column=1, row=0)

# ----WEBSITE LABEL-------
website = Label(text='Website:', bg='white', fg='black')
website.grid(column=0, row=1)

# ----WEBSITE ENTRY------

web_entry = Entry(width=18, bg='white', insertbackground='black', fg='black', highlightthickness=1)
web_entry.focus()
web_entry.grid(column=1, columnspan=1, row=1)

# ---- SEARCH BUTTON -----------
search = Button(text='Search', fg='black', bg='white', highlightthickness=0, highlightbackground='white', width=14,
                command=search)
search.grid(column=2, row=1)

# ---EMAIL/USERNAME LABEL-----
email = Label(text='Email/Username:', bg='white', fg='black')
email.grid(column=0, row=2)

# ----EMAIL ENTRY--------------
email_entry = Entry(width=35, bg='white', insertbackground='black', fg='black', highlightthickness=1)
email_entry.insert(0, string="deepika.see@gmail.com")
email_entry.grid(column=1, columnspan=2, row=2)

# ---PASSWORD LABEL -----------
password = Label(text='Password:', bg='white', fg='black')
password.grid(column=0, row=3)

# ----PASSWORD ENTRY--------------
password_entry = Entry(width=18, bg='white', insertbackground='black', fg='black', highlightthickness=1)
password_entry.grid(column=1, columnspan=1, row=3)

# ------ GENERATE PASSWORD --------
generate = Button(text='Generate Password', fg='black', bg='white', highlightthickness=0, highlightbackground='white',
                  command=password_gen)
generate.grid(column=2, row=3)

# -----ADD BUTTON -----------------
add = Button(text='Add', fg='black', bg='white', highlightbackground='white', width=36, command=save_data)
add.grid(column=1, row=4, columnspan=2)

windows.mainloop()
