from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def create_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    letters_list = [random.choice(letters) for a in range(nr_letters)]

    symbol_list = [random.choice(symbols) for b in range(nr_symbols)]

    numbers_list = [random.choice(numbers) for c in range(nr_numbers)]

    password_list = letters_list + symbol_list + numbers_list

    random.shuffle(password_list)


    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().capitalize()
    email = email_entry.get()
    password = password_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data_dict = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")

    else:
        if website in data_dict:
            search_email = data_dict[website]["email"]
            search_password = data_dict[website]["password"]
            pyperclip.copy(search_password)
            messagebox.showinfo(title=website,
                                message=f"email: {search_email}\npassword: {search_password}\n\nThe password has been copied to clipboard.")
        else:
            if website == "":
                messagebox.showinfo(title="Error", message="The website field is left empty.")
            else:
                messagebox.showinfo(title="Error", message="No details for the website exists.")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_entries():
    website = website_entry.get().capitalize()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {f"{website}": {
                "email": f"{email}",
                "password": f"{password}"}}

    if website == "" or password == "" or email == "":
        empty_message = messagebox.showinfo(title="Error", message="Some fields are left empty. Please check again.")

    else:
        yes_message = messagebox.askyesno(title=website,
                                          message=f"Please confirm the details-\n\n  Email: {email}\n  Password: {password}\n\nProceed?")
        if yes_message == True:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                messagebox.showinfo(title="Password", message="Saving data successful. The password has been copied to clipboard.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")

canvas = Canvas()
canvas.config(width=200, height=200)
lock_image = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(row=0, column=1)

#Labels
website_label = Label(text="Website:")
website_label.grid(row=1,column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

#Entries
website_entry = Entry(width=33)
website_entry.grid(row=1, column=1)

email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "prateek2004@gmail.com")

password_entry = Entry(width=33)
password_entry.grid(row=3, column=1,)

#Buttons
search_button = Button(text="Search",bg="gainsboro", highlightthickness=0, command=find_password, width=15)
search_button.grid(row=1, column=2)

generate_password = Button(text="Generate Passsword", highlightthickness=0, bg="gainsboro", command=create_password, width=15)
generate_password.grid(row=3, column=2)

add_button = Button(text="Add", width=36, bg="gainsboro", command=save_entries)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()