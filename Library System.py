from tkinter import *
from datetime import *
from tkinter import messagebox

# Defining functions ----------------------------------------------------------------------------------------------------------------------------------------


# Return function
def back():
    window3.destroy()
    login()


# Feedback
def send():
    report = str(feedback.get("1.0", END))
    with open("feedback.txt", "a") as w:
        w.write(report)

    feedback.delete("1.0", END)


# Borrow book function
def book_borrow():
    user_borrow = str(borrow.get())
    books = []
    author = []
    code = []
    availability = []

    with open("availability.txt", "r") as f:
        for lines in f:
            book = lines[:-1].split("|")
            code.append(book[3])
            availability.append(book[2])
            author.append(book[1])
            books.append(book[0])

    if user_borrow in code:
        borrow_date = datetime.now()
        return_date = borrow_date + timedelta(days=14)
        idx = code.index(user_borrow)

        if availability[idx] == "0":
            messagebox.showinfo(
                "Library System", "We're sorry, the book you've requested had been borrowed.")

        else:
            with open("borrow.txt", "r") as f:
                f_contents = f.read()

                if (login_username in f_contents) and (user_borrow in f_contents):
                    messagebox.showinfo("Library System", "You have already borrowed the book.")

                else:
                    one.insert(END, "Book Title: " + books[idx])
                    one.insert(END, "Borrow Date: " + borrow_date.strftime("%A,%d %B %Y"))
                    one.insert(END, "Borrow Time: " + borrow_date.strftime("Time: %H:%M:%S"))
                    one.insert(END, "Return Date: " + return_date.strftime("%A,%d %B %Y"))
                    one.insert(END, "Return Time: " + return_date.strftime("Time: %H:%M:%S" + "\n"))
                    one.insert(END, "\n")
                    one.pack()

                    with open("borrow.txt", "a") as z:
                        z.write("Borrowed By|" + login_username + "|Book name|" +
                                books[idx] + "|Book code|" + user_borrow + "|Return Date|" + str(return_date.strftime("%A,%d %B %Y")) + "\n")

                    availability[idx] = str(int(availability[idx])-1)

                    with open("availability.txt", "w+") as r:
                        r.seek(0)
                        for i in range(len(books)):
                            r.write("%s|%s|%s|%s\n" %
                                    (books[i], author[i], availability[i], code[i]))

    else:
        messagebox.showerror("Error", "Invalid entry!")

    entry7.delete(0, END)


# Return book function
def book_return():
    returns = str(ret.get())

    # borrow.txt
    user = []
    code_borrow = []
    date = []
    bookname = []
    a = []
    b = []
    c = []

    # availability.txt
    code = []
    availability = []
    author = []
    books = []

    with open("borrow.txt", "r") as f:
        f_contents = f.read()

    with open("borrow.txt", "r") as f:
        for lines in f:
            brw = lines[:-1].split("|")
            user.append(brw[1])
            a.append(brw[2])
            bookname.append(brw[3])
            b.append(brw[4])
            code_borrow.append(brw[5])
            c.append(brw[6])
            date.append(brw[7])

    with open("availability.txt", "r") as f:
        for lines in f:
            book = lines[:-1].split("|")
            code.append(book[3])
            availability.append(book[2])
            author.append(book[1])
            books.append(book[0])

    if (login_username in f_contents) and (returns in f_contents):
        idx = code_borrow.index(returns)
        del user[idx]
        del code_borrow[idx]
        del date[idx]
        del bookname[idx]
        del a[idx]
        del b[idx]
        del c[idx]

        with open("borrow.txt", "w+") as f:
            f.seek(0)
            for i in range(len(user)):
                f.write("Borrowed By|" + user[i] + "|Book name|" + bookname[i] +
                        "|Book code|" + code_borrow[i] + "|Return Date|" + str(date[i]) + "\n")

        availability[idx] = str(int(availability[idx])+1)

        with open("availability.txt", "w+") as r:
            r.seek(0)
            for i in range(len(books)):
                r.write("%s|%s|%s|%s\n" %
                        (books[i], author[i], availability[i], code[i]))

        show.insert(END, "You have successfully returned " + returns + ", thank you!" + "\n")

    else:
        messagebox.showerror("Error", "Invalid entry!")

    entry8.delete(0, END)


# Login Menu function
def login1():
    global borrow
    global window3
    global ret
    global entry7
    global entry8
    global feedback
    global one
    global two
    global show

    window3 = Toplevel(window)
    window3.configure(background='Gainsboro')
    window3.geometry("1280x720")
    scrollbar2 = Scrollbar(window3)
    scrollbar2.pack(side=RIGHT, fill=Y)
    login_choice = str(log_choice.get())

    # 1. Borrow book
    if login_choice == "1":
        window2.destroy()
        borrow = StringVar()

        Label(window3, text="Enter code of book you would like to borrow", justify=CENTER,
              bg="Gainsboro", fg="Black", font=("Calibri Light Bold", 16)).pack()
        Label(window3, text="", bg="Gainsboro").pack()
        entry7 = Entry(window3, textvariable=borrow, justify=CENTER)
        entry7.pack()
        Label(window3, text="", bg="Gainsboro").pack()
        Button(window3, text="Borrow", width="10", height="1", command=book_borrow).pack()
        Label(window3, text="", bg="Gainsboro").pack()
        Button(window3, text="Back", width="10", height="1", command=back).pack()
        one = Listbox(window3, yscrollcommand=scrollbar2.set, bg="Gainsboro", fg="Green", width=60,
                      height=15, justify=CENTER, font=("Calibri Light Bold", 16))
        one.pack()
        Label(window3, text="", bg="Gainsboro").pack()
        scrollbar2.config(command=one.yview)

    # 2. Return book
    elif login_choice == "2":
        user = []
        code_borrow = []
        date = []
        bookname = []

        with open("borrow.txt", "r") as f:
            for lines in f:
                brw = lines[:-1].split("|")
                user.append(brw[1])
                bookname.append(brw[3])
                code_borrow.append(brw[5])
                date.append(brw[7])

        ret = StringVar()

        if (login_username in user):
            window2.destroy()
            idx = user.index(login_username)
            show = Listbox(window3, yscrollcommand=scrollbar2.set, bg="Gainsboro", fg="Green", width=60,
                           height=15, justify=CENTER, font=("Calibri Light Bold", 16))
            show.pack()
            show.insert(END, "Name: " + user[idx])
            show.insert(END, "Book Borrowed: " +
                        bookname[idx])
            show.insert(END, "Return date: " + date[idx])
            show.insert(END, "\n")
            Label(window3, text="", bg="Gainsboro").pack()
            Label(window3, text="Enter book code to return", bg="Gainsboro", fg="Black",
                  anchor=CENTER, justify=LEFT, font=("Calibri Light Bold", 16)).pack()
            Label(window3, text="", bg="Gainsboro").pack()
            entry8 = Entry(window3, textvariable=ret, justify=CENTER)
            entry8.pack()
            Label(window3, text="", bg="Gainsboro").pack()
            Button(window3, text="Return", width="10", height="1", command=book_return).pack()
            Label(window3, text="", bg="Gainsboro").pack()
            Button(window3, text="Back", width="10", height="1", command=back).pack()
            scrollbar2.config(command=show.yview)

        else:
            Label(window2, text="\nYou have not borrowed any books", bg="Gainsboro",
                  fg="Red", anchor=CENTER, justify=LEFT, font=("Calibri Light Bold", 16)).pack()
            window3.destroy()
            entry6.delete(0, END)

    # 3. Feedback/Report
    elif login_choice == "3":
        window2.destroy()
        Label(window3, text="\n\n\nPlease enter your Feedback/Report below", bg="Gainsboro",
              fg="Green", anchor=CENTER, justify=LEFT, font=("Calibri Light Bold", 16)).pack()
        Label(window3, text="", bg="Gainsboro").pack()
        Label(window3, text="", bg="Gainsboro").pack()
        feedback = Text(window3, width=60, height=10)
        feedback.pack()
        Label(window3, text="", bg="Gainsboro").pack()
        Button(window3, text="Send", width="10", height="1", command=send).pack()
        Label(window3, text="", bg="Gainsboro").pack()
        Button(window3, text="Back", width="10", height="1", command=back).pack()

    else:
        Label(window3, text="Invalid Input", bg="Gainsboro",
              fg="Red", font=("Calibri Light Bold", 16)).pack()
        window2.destroy()


# User login function
def login():
    global log_choice
    global login1
    global entry6
    global window2
    global login_username

    window2 = Toplevel(window)
    window2.configure(background='Gainsboro')
    window2.geometry("1280x720")
    window.iconify()

    log_choice = StringVar()
    login_username = str(log_username.get())
    login_password = str(log_password.get())

    with open("accounts.txt", "r") as f:
        f_contents = f.read()
        f_contents.rstrip('\n')

    # Login Criteria
    if (login_username in f_contents) and (login_password in f_contents):
        Label(window2, text="\n\n\nWelcome back " + login_username,
              bg="Gainsboro", fg="Green", font=("Calibri Light Bold", 22)).pack()
        Label(window2, text="", bg="Gainsboro").pack()
        Label(window2, text="What would you like to do?", bg="Gainsboro",
              fg="Green", font=("Calibri Light Bold", 16)).pack()
        Label(window2, text="\n1. Check-Out\n2. Return\n3. Feedback/Report",
              fg="Black", bg="Gainsboro", anchor=CENTER, justify=LEFT, font=("Calibri Light Bold", 16)).pack()
        Label(window2, text="", bg="Gainsboro").pack()
        entry6 = Entry(window2, textvariable=log_choice, justify=CENTER)
        entry6.pack()
        Label(window2, text="", bg="Gainsboro").pack()
        Button(window2, text="Enter", width="10", height="1", command=login1).pack()
        window1.destroy()

    elif login_password not in f_contents:
        Label(window1, text="Invalid Password!", bg="Gainsboro",
              fg="Red", font=("Calibri Light Bold", 16)).pack()
        window2.destroy()

        entry4.delete(0, END)
        entry5.delete(0, END)

    elif login_username not in f_contents:
        Label(window1, text="Invalid Username!", bg="Gainsboro",
              fg="Red", font=("Calibri Light Bold", 16)).pack()
        window2.destroy()

        entry4.delete(0, END)
        entry5.delete(0, END)

    else:
        Label(window1, text="Invalid Username and Password!", bg="Gainsboro",
              fg="Red", font=("Calibri Light Bold", 16)).pack()
        window2.destroy()

        entry4.delete(0, END)
        entry5.delete(0, END)


# Create account function
def enter():
    user_username = str(username.get())
    user_password = str(password.get())

    with open("accounts.txt", "r") as f:
        f_contents = f.read()

    with open("accounts.txt", "a") as a:
        a.write("|" + user_username + "|" + user_password)

    if user_username in f_contents:
        Label(window1, text="\nUsername already exists, choose another.",
              bg="Gainsboro", fg="Red", font=("Calibri Light Bold", 16)).pack()

    else:
        Label(window1, text="\nAccount Successfully Created!", bg="Gainsboro",
              fg="Green", font=("Calibri Light Bold", 16)).pack()

    entry2.delete(0, END)
    entry3.delete(0, END)


# Search book function
def search_code():
    books = []
    author = []
    availability = []
    code = []

    user_code = str(book_code.get())

    with open("availability.txt", "r") as f:
        for lines in f:
            line = lines[:-1].split('|')
            books.append(line[0])
            author.append(line[1])
            availability.append(line[2])
            code.append(line[3])

    if user_code in code:
        idx = code.index(user_code)
        if availability[idx] != "0":
            display.insert(END, "Requested book: " + books[idx] + ", available!")

        else:
            display.insert(END, "Requested book: " + books[idx] + ", unavailable!")

    else:
        messagebox.showerror("Error", "Invalid entry!")

    entry1.delete(0, END)


# Main menu options function
def go():
    global window1
    global book_borrow
    global display

    window1 = Toplevel(window)
    window1.configure(background="black")
    window1.geometry("1280x720")
    user_option = str(menu_option.get())

    # 1. Book List
    if user_option == "1":
        scrollbar = Scrollbar(window1)
        scrollbar.pack(side=RIGHT, fill=Y)
        menu_entry.delete(0, END)

        listbox = Listbox(window1, yscrollcommand=scrollbar.set, width=210, height=310,
                          justify=CENTER, bg="black", fg="light green", font=("Consolas", 12))
        listbox.pack()

        with open("books.txt", "r") as f:
            f_contents = f.readlines()

        for i in range(len(f_contents)):
            listbox.insert(END, f_contents[i])

        scrollbar.config(command=listbox.yview)

    # 2. Search
    elif user_option == "2":
        global book_code
        global entry1

        window1.configure(background="Gainsboro")
        scrollbar3 = Scrollbar(window1)
        scrollbar3.pack(side=RIGHT, fill=Y)
        book_code = StringVar()
        menu_entry.delete(0, END)

        Label(window1, text="Enter the book code below to identify the book.", bg="Gainsboro",
              fg="Black", anchor=CENTER, justify=CENTER, font=("Calibri", 15)).pack()
        Label(window1, text="", bg="Gainsboro").pack()
        entry1 = Entry(window1, textvariable=book_code, justify=CENTER)
        entry1.pack()
        Label(window1, text="", bg="Gainsboro").pack()
        Button(window1, text="Search", width="10", height="1", command=search_code).pack()
        display = Listbox(window1, yscrollcommand=scrollbar3.set, bg="Gainsboro", fg="Black", width=60,
                          height=15, justify=CENTER, font=("Calibri Light Bold", 16))
        display.pack()
        scrollbar3.config(command=display.yview)

    # 3. Create Account
    elif user_option == "3":
        global username
        global password
        global entry2
        global entry3

        window1.configure(background='Gainsboro')
        username = StringVar()
        password = StringVar()
        menu_entry.delete(0, END)

        Label(window1, text="\n\nEnter Username", bg="Gainsboro",
              fg="Black", font=("Calibri Light Bold", 16)).pack()
        entry2 = Entry(window1, textvariable=username, justify=CENTER)
        entry2.pack()
        Label(window1, text="", bg="Gainsboro").pack()
        Label(window1, text="Enter Password", bg="Gainsboro",
              fg="Black", font=("Calibri Light Bold", 16)).pack()
        Label(window1, text="", bg="Gainsboro").pack()
        entry3 = Entry(window1, textvariable=password, justify=CENTER)
        entry3.pack()
        Label(window1, text="", bg="Gainsboro").pack()
        Button(window1, text="Go", width="10", height="1", command=enter).pack()
        Label(text="", bg="Gainsboro").pack()

    # 4. Login
    elif user_option == "4":
        global log_username
        global log_password
        global entry4
        global entry5

        window1.configure(background='Gainsboro')
        log_username = StringVar()
        log_password = StringVar()
        menu_entry.delete(0, END)

        Label(window1, text="\n\nEnter Username: ", bg="Gainsboro",
              fg="Black", font=("Calibri Light Bold", 16)).pack()
        entry4 = Entry(window1, textvariable=log_username, justify=CENTER)
        entry4.pack()
        Label(window1, text="", bg="Gainsboro").pack()
        Label(window1, text="Enter Password: ", bg="Gainsboro",
              fg="Black", font=("Calibri Light Bold", 16)).pack()
        entry5 = Entry(window1, textvariable=log_password, justify=CENTER)
        entry5.pack()
        Label(window1, text="", bg="Gainsboro").pack()
        Button(window1, text="Go", width="10", height="1", command=login).pack()
        Label(text="", bg="Gainsboro").pack()

    # 5. Exit
    elif user_option == "5":
        window.destroy()

    # 6. Avoid Error
    else:
        menu_entry.delete(0, END)
        Label(window, text="\nInvalid Input!", bg="Gainsboro",
              fg="Red", font=("Calibri Light Bold", 16)).pack()
        window1.destroy()


# Main screen
def main_screen():
    global window
    global menu_option
    global menu_entry

    window = Tk()
    window.title("XXX's Library System")
    window.configure(background='Gainsboro')
    window.geometry("1280x720")
    menu_option = StringVar()

    Label(text="\n\n\nWelcome to XXX's Library System".upper(),
          bg="Gainsboro", fg="Black", font=("Arial Black", 20)).pack()
    Label(text="", bg="Gainsboro").pack()
    Label(text="What would you like to do? \n\n1. Book List\n2. Search\n3. Create Account\n4. Log-In\n5. Exit",
          fg="Black", bg="Gainsboro", anchor=CENTER, justify=LEFT, font=("Calibri Light Bold", 16)).pack()
    Label(text="", bg="Gainsboro").pack()
    menu_entry = Entry(window, textvariable=menu_option, justify=CENTER)
    menu_entry.pack()
    Label(text="", bg="Gainsboro").pack()
    Button(window, text="Go", width="10", height="1", command=go).pack()
    Label(text="", bg="Gainsboro").pack()
    window.mainloop()


main_screen()
