# Initializing the GUI window
from collections import namedtuple

import Phonebook as pb
import tkinter as tk
import uuid
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

window = Tk()                                                                                          # A window is an instance of Tkinter's Tk class
window.title("Phone Book")
window.geometry('750x550')

# Create Frames
frame_up = Frame(window, width=500, height=50, bg='lightblue')
frame_up.grid(row=0, column=0, padx=0, pady=1, columnspan=2, sticky="NESW")

frame_middle = Frame(window, width=500, height=200)
frame_middle.grid(row=1, column=0, padx=0, pady=1)

frame_bottom = Frame(window, width=500, height=300)
frame_bottom.grid(row=3, column=0, padx=0, pady=1)

frame_table = Frame(window, width=400, height=300)
frame_table.grid(row=4, column=0, padx=100, pady=20)

# Create Labels inside the frames
l_phonebook = Label(frame_up, text='Phonebook', height=1, font=('Verdana 17 bold'), bd=10, bg='lightblue')
l_phonebook.grid(row=0, column=0)
frame_up.columnconfigure(0, weight=1)
frame_up.rowconfigure(0, weight=1)

l_firstname = Label(frame_middle, font=("Aerial", 10), text='First name', height=1)
l_firstname.place(x=20, y=80)

l_lastname = Label(frame_middle, font=("Aerial", 10), text='Last name', height=1)
l_lastname.place(x=20, y=110)

l_phone = Label(frame_middle,  font=("Aerial", 10), text='Mobile number', height=1)
l_phone.place(x=20, y=140)

#  Creating entry objects
e_firstname = Entry(frame_middle, bd=5, width=25,  font=('calibre', 10, 'normal'), justify='left')
e_firstname.place(x=140, y=80)

e_lastname = Entry(frame_middle, bd=5,  font=('calibre', 10, 'normal'), width=25, justify='left')
e_lastname.place(x=140, y=110)

e_phone = Entry(frame_middle, bd=5,  font=('calibre', 10, 'normal'), width=25, justify='left')
e_phone.place(x=140, y=140)

# creating Phonebook class object and loading existing json data
phb_obj = pb.Phonebook()                                                                                # creating class Phonebook object
phb_obj.load()                                                                                          # calling load function of the class Phonebook to read the json file


def add_con():
    if e_firstname.get() and e_lastname.get() and e_phone.get():
        phb_obj.load()
        cont = pb.Contact(str(uuid.uuid4()), e_firstname.get(), e_lastname.get(), e_phone.get())
        phb_obj.add(cont)
        e_firstname.delete(0, 'end')
        e_lastname.delete(0, 'end')
        e_phone.delete(0, 'end')
        e_firstname.focus()
        phb_obj.save()
        phb_obj.load()
        clear_table()
        render_table()
    else:
        messagebox.showinfo("Info", "First name, Last name and Phone are mandatory fields!")


b_add = Button(frame_bottom, text='Add', width=10, font=("Aerial", 10), activebackground="orange", command=add_con)
b_add.pack(side='left')


# creating Treeview to display data in table format
list_header = ["id", "fname", "lname", "phone"]
table_scroll = Scrollbar(frame_table)                                               # creating scrollbar for the table
table_scroll.pack(side=RIGHT, fill=Y)
table = ttk.Treeview(frame_table, yscrollcommand=table_scroll.set)                  # set the treeview object

# define our column
table['columns'] = ('id', 'fname', 'lname', 'phone')
# format our column
table.column("id", anchor=CENTER, minwidth=0, width=0)
table.column("fname", anchor=CENTER, width=100)
table.column("lname", anchor=CENTER, width=100)
table.column("phone", anchor=CENTER, width=120)
# Create Heading
table.heading("id", text="Id", anchor=CENTER)
table.heading("fname", text="First name", anchor=W)
table.heading("lname", text="Last name", anchor=CENTER)
table.heading("phone", text="Contact number", anchor=CENTER)


def item_selected(event):
    for selected_item in table.selection():
        item = table.item(selected_item)
        record = item['values'][0]
        name = item['values'][1]
        txt = "Do you want to delete {}'s contact information?" + str(event)
        # show a message
        res = messagebox.askquestion(title='Delete', message=txt.format(name))
        if res == 'yes':
            phb_obj.delete_cont(record)
            phb_obj.save()
            phb_obj.load()
            clear_table()
            render_table()


table.bind('<<TreeviewSelect>>', item_selected)


def render_table():
    for dic in phb_obj.data:
        contact = namedtuple("Contact", dic.keys())(*dic.values())
        table.insert('', tk.END, values=(contact.id, contact.fname, contact.lname, contact.phone))
    table.pack()


def clear_table():
    for row in table.get_children():
        table.delete(row)


render_table()
window.mainloop()

