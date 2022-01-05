from tkinter import *
from tkinter import messagebox
import password_generator
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_input.delete(0, 'end')
    generated_password = password_generator.generate_password()
    password_input.insert(0, generated_password)
    pyperclip.copy(generated_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website_i = website_input.get().lower()
    username_i = username_input.get()
    password_i = password_input.get()
    new_data = {
        website_i: {
            "email/username": username_i,
            "password": password_i,
        }
    }
    if 0 in (len(website_i), len(username_i), len(password_i)):
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website_i, message=f"These are the detail entered: \n"
                                                                f"email/username: {username_i}\n"
                                                                f"password: {password_i}\n"
                                                                f"Do you want to save?")
        if is_ok:
            try:
                with open("passwords.json", "r") as password_storage:
                    data = json.load(password_storage)
                    data.update(new_data)
                with open("passwords.json", "w") as password_storage:
                    json.dump(data, password_storage, indent=4)
            except FileNotFoundError:
                with open("passwords.json", "w") as password_storage:
                    json.dump(new_data, password_storage, indent=4)
            finally:
                website_input.delete(0, 'end')
                password_input.delete(0, 'end')


# Search for existing data

def search():
    website_search = website_input.get()
    try:
        with open("passwords.json") as password_storage:
            data = json.load(password_storage)
            name = data.get(website_search.lower())
        username_input.delete(0, END)
        print(name.get("email/username"))
        username_input.insert(0, name.get('email/username'))
        password_input.delete(0, END)
        password_input.insert(0, name.get('password'))
    except AttributeError:
        messagebox.showerror(title="Oops", message="Website name has no data saved!")
    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="Currently no data has been loaded yet!")
    else:
        messagebox.showinfo(title="Load Successful", message="Website account information has been loaded!")

    # ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.config(padx=20, pady=20)
canvas = Canvas(width=200, height=200)
lock_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(column=1, row=0)

website = Label(text="Website:")
website.grid(column=0, row=1)
website_input = Entry()
website_input.grid(column=1, row=1, sticky="EW")
website_input.focus()
search = Button(text="Search", command=search)
search.grid(column=2, row=1, sticky="EW")

username = Label(text="Email/Username:")
username.grid(column=0, row=2)
username_input = Entry()
username_input.insert(0, "alexlee78980@gmail.com")
username_input.grid(column=1, row=2, columnspan=2, sticky="EW")

password = Label(text="Password:")
password.grid(column=0, row=3)
password_input = Entry(width=21)
password_input.grid(column=1, row=3, sticky="EW")
generate = Button(text="Generate Password", command=generate_password)
generate.grid(column=2, row=3, sticky="EW")

add_button = Button(text="Add", width=36, command=save_password)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")
window.mainloop()
