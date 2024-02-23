from tkinter import *
from tkinter import messagebox
import csv
from operator import itemgetter

global fnamecontent, numcontent, nnamecontent, nnumbercontent
writeList = []


def csvRead():
    global x
    try:
        file = open('book.csv', "r")
        csvRead = csv.reader(file)
        for row in csvRead:
            writeList.append(row)
        print(len(writeList), 'contacts available ')
        file.close()

    except:
        file = open("book.csv", 'w', newline='')
        file.close()


def initialise():
    writeList.clear()
    csvRead()
    listboxname.delete(0, END)
    for i in writeList:
        if len(i) > 0:
            listboxname.insert(END, f'{i[0]} - {i[1]}')
    listboxname.selection_clear(0, END)


def csvWrite(writeList):
    with open("book.csv", 'w', newline='') as file:
        csv_w = csv.writer(file, delimiter=',')
        for i in sorted(writeList, key=itemgetter(0)):
            csv_w.writerow(i)
    initialise()


def checkcom():
    global ck_em, ck_ad, add, frame_email, frame_address, visibleE, visibleA, emailentry, addressentry
    h = 180
    if ck_em.get() == 1:
        h += 40
        add.geometry("510x{}+{}+{}".format(h, root.winfo_x() + 100, root.winfo_x()))
        frame_email.pack()
        emailentry.delete(0, END)
        visibleE = 1
    if ck_em.get() == 0:
        h + -40
        add.geometry("510x{}+{}+{}".format(h, root.winfo_x() + 100, root.winfo_x()))
        frame_email.pack_forget()
        visibleE = 0
    if ck_ad.get() == 1:
        h += 40
        add.geometry("510x{}+{}+{}".format(h, root.winfo_x() + 100, root.winfo_x()))
        frame_address.pack()
        addressentry.delete(0, END)
        visibleA = 1
    if ck_ad.get() == 0:
        h + -40
        add.geometry("510x{}+{}+{}".format(h, root.winfo_x() + 100, root.winfo_x()))
        frame_address.pack_forget()
        visibleA = 0


def addpop():
    global fnameentry, numentry, emailentry, addressentry, add, ck_em, ck_ad, frame_email, frame_address

    add = Toplevel(root)
    add.geometry("510x180+{}+{}".format(root.winfo_x() + 100, root.winfo_x()))
    add.title("Add Contact")
    add.resizable(False, False)
    frame1 = LabelFrame(add, text="Enter New Contact Details", width="310")
    frame1.place(x=10, y=10)

    ck_em = IntVar()
    ck_ad = IntVar()

    frame_name = Frame(frame1, height=10)
    frame_name.pack()
    fnamelabel = Label(frame_name, text="Enter full name:")
    fnamelabel.pack(side=LEFT, padx=10, anchor='w')
    fnameentry = Entry(frame_name, textvariable=fnamecontent, width="41")
    fnameentry.pack(side=RIGHT, pady=10, padx=10)
    fnameentry.focus()

    frame_number = Frame(frame1)
    frame_number.pack()
    fnamelabel = Label(frame_number, text="Enter number:   ")
    fnamelabel.pack(side=LEFT, padx=10)
    numentry = Entry(frame_number, textvariable=numbercontent, width="41")
    numentry.pack(side=RIGHT, pady=10, padx=10)

    frame_email = Frame(frame1)
    femaillabel = Label(frame_email, text="Enter Email:       ")
    femaillabel.pack(side=LEFT, padx=10)
    emailentry = Entry(frame_email, textvariable=emailcontent, width="41")
    emailentry.pack(side=RIGHT, pady=10, padx=10)

    frame_address = Frame(frame1)
    faddresslabel = Label(frame_address, text="Enter address:   ")
    faddresslabel.pack(side=LEFT, padx=10)
    addressentry = Entry(frame_address, textvariable=addresscontent, width="41")
    addressentry.pack(side=RIGHT, pady=10, padx=10)

    frame_button = Frame(add)
    frame_button.pack(side=BOTTOM, pady=10)
    frame_check = Frame(frame_button)
    frame_check.pack(side=LEFT, anchor="sw")
    checkem = Checkbutton(frame_check, text="Add Email",
                          variable=ck_em, onvalue=1, offvalue=0, command=checkcom)
    checkem.pack(side=LEFT)
    checkad = Checkbutton(frame_check, text="Add Address",
                          variable=ck_ad, onvalue=1, offvalue=0, command=checkcom)
    checkad.pack(side=LEFT)
    submit = Button(frame_button, text="Add", width='10', bg="light blue", command=addcontact)
    submit.pack(side=LEFT, padx=10)
    cancel = Button(frame_button, text="Cancel", width='10', bg="light blue", command=add.destroy)
    cancel.pack(side=LEFT, padx=10)


def addcontact():
    global fnameentry, numentry, emailentry, addressentry, add, visibleE, visibleA
    name = str(fnameentry.get().rstrip())
    num = numentry.get().rstrip()
    email = emailentry.get().rstrip()
    address = addressentry.get().rstrip()
    visibleE = 0
    visibleA = 0
    if len(email) == 0:
        email = "-"
    if len(address) == 0:
        address = "-"
    if len(name) != '' and num != '':
        try:
            int(num)
            writeList.append([name, num, email, address])
            print(f'Details for {name}', 'added.')
            csvWrite(writeList)
            fnameentry.delete(0, END)
            numentry.delete(0, END)
            if visibleE == 1:
                emailentry.delete(0, END)
            if visibleA == 1:
                addressentry.delete(0, END)
            add.destroy()
            listboxname.selection_clear(0, END)
        except:
            messagebox.showerror("Error", "Invalid number")
            numbercontent.set('')
            add.focus()
    else:
        messagebox.showerror("Error", "Please Enter the Information")
        fnameentry.focus()


def view():
    try:
        currIndex = int(listboxname.curselection()[0])
        i = writeList[currIndex]
        new = ('Name: {}\nNumber: {}\nEmail: {}\nAddress: {}'.format(i[0], i[1], i[2], i[3]))
        messagebox.showinfo("Search", new)
    except:
        messagebox.showerror("Error", "Select a contact to View.")


def remove():
    global csvRead
    try:
        currIndex = int(listboxname.curselection()[0])
        item = listboxname.get(ANCHOR)
        choice = messagebox.askyesno('Confirmation', 'Do you want to delete this contact?')
        if choice == True:
            print(writeList[currIndex][0], 'removed.')
            listboxname.delete(ANCHOR)
            data = []
            del writeList[currIndex]
            csvWrite(writeList)
            listboxname.selection_clear(0, END)
    except:
        messagebox.showerror("Error", "Please select a contact to Delete.")


def update():
    global item, nnamecontent, nnumbercontent, nemailcontent, naddresscontent, newup, nnameentry, nnumentry, nemailentry, naddressentry
    item = listboxname.get(ANCHOR)
    if len(item) == 0:
        messagebox.showerror("Error", "Select a contact to Update.")
    else:
        currIndex = int(listboxname.curselection()[0])
        print('Old Contact', writeList[currIndex])

        # --------Update pop-up--------
        newup = Toplevel(root)
        newup.geometry("405x227+{}+{}".format(root.winfo_x() + 100, root.winfo_x()))
        newup.focus()
        newup.resizable(False, False)

        nnamecontent = StringVar()
        nnumbercontent = StringVar()
        nemailcontent = StringVar()
        naddresscontent = StringVar()

        mini_frame = Frame(newup)
        mini_frame.place(x=0, y=0)
        nnamelabel = Label(mini_frame, text="Enter new name:    ")
        nnamelabel.pack(fill=X, side=LEFT, padx=10)
        nnameentry = Entry(mini_frame, textvariable=nnamecontent, width="29")
        nnameentry.pack(fill=X, side=RIGHT, pady=10, padx=10)
        nnameentry.focus()

        frame_number = Frame(newup)
        frame_number.place(x=0, y=40)
        fnamelabel = Label(frame_number, text="Enter new number:")
        fnamelabel.pack(fill=X, side=LEFT, padx=10)
        nnumentry = Entry(frame_number, textvariable=nnumbercontent, width="29")
        nnumentry.pack(fill=X, side=RIGHT, pady=10, padx=10)

        frame_number = Frame(newup)
        frame_number.place(x=0, y=80)
        femaillabel = Label(frame_number, text="Enter new Email:    ")
        femaillabel.pack(fill=X, side=LEFT, padx=10)
        nemailentry = Entry(frame_number, textvariable=nemailcontent, width="29")
        nemailentry.pack(fill=X, side=RIGHT, pady=10, padx=10)

        frame_number = Frame(newup)
        frame_number.place(x=0, y=120)
        faddresslabel = Label(frame_number, text="Enter new Address:")
        faddresslabel.pack(fill=X, side=LEFT, padx=10)
        naddressentry = Entry(frame_number, textvariable=naddresscontent, width="29")
        naddressentry.pack(fill=X, side=RIGHT, pady=10, padx=10)

        exitb = Button(newup, text="Update", width="15", command=replace)
        exitb.place(x=10, y=165)

        Label(newup, text="Note: Keep blank if particular entry shall remain same.").pack(side=BOTTOM, anchor="sw")


def replace():
    global csvRead, item, newup, nnameentry, nnnumentry, nemailentry, naddressentry
    currIndex = int(listboxname.curselection()[0])
    name = nnameentry.get()
    num = nnumentry.get()
    email = nemailentry.get()
    address = naddressentry.get()
    if len(num) == 0:
        num = writeList[currIndex][1]
    if len(name) == 0:
        name = writeList[currIndex][0]
    if len(email) == 0:
        email = writeList[currIndex][2]
    if len(address) == 0:
        address = writeList[currIndex][3]
    print('New: ', [name, num, email, address])
    writeList[currIndex] = [name, num, email, address]
    csvWrite(writeList)
    newup.destroy()
    listboxname.selection_clear(0, END)


def find():
    global fentry, find_top, entry
    fentry = StringVar()
    find_top = Toplevel(root)
    find_top.resizable(False, False)
    find_top.title('Find Contact')
    find_top.geometry("300x145+%d+%d" % (root.winfo_x() + 100, root.winfo_x()))
    Label(find_top, text="Enter the name or number", font="Calibri 10").place(x=10, y=10)
    entry = Entry(find_top, width=26, font="Calibri 12", textvariable=fentry)
    entry.place(x=10, y=50)
    entry.focus()
    Button(find_top, text="Search", width='10', command=mark).place(x=10, y=94)
    listboxname.selection_set


def mark():
    global fentry, find_top, entry
    listboxname.selection_clear(0, END)
    var = fentry.get()
    try:
        if var != '':
            c = 0
            got = 0
            new = ''
            if var.isnumeric():
                for i in writeList:
                    if i[1] == var:
                        new += ('{} - {}\n'.format(i[0], i[1]))
                        listboxname.selection_set(c)
                        got = 1
                    c += 1
            else:
                for i in writeList:
                    if i[0].upper() == var.upper():
                        new += ('{} - {}\n'.format(i[0], i[1]))
                        listboxname.selection_set(c)
                        got = 1
                    c += 1
        if got == 1:
            messagebox.showinfo("Search", new)
        else:
            messagebox.showwarning("Search", 'No Contacts Found')
        find_top.destroy()
    except:
        messagebox.showwarning("Search", 'Enter a name or number to find.')
        entry.focus()


root = Tk()
height = 300
width = 504
x = (root.winfo_screenwidth() // 2 - width // 2)
y = (root.winfo_screenheight() // 2 - height)
root.geometry("{}x{}+{}+{}".format(width, height, x, y))
root.title("Phonebook")

##----------

fnamecontent = StringVar()
numbercontent = StringVar()
emailcontent = StringVar()
addresscontent = StringVar()
##-----Buttons Section--------
frame_button = Frame(root)
frame_button.place(x=10, y=248)
button_submit = Button(frame_button, activebackground="#84e389", text="ADD", width='10', bg="light blue",
                       command=addpop)
button_submit.pack(side=LEFT, padx=4, pady=10)
button_view = Button(frame_button, activebackground="#84e389", text="View", width='10', bg="light Blue", command=view)
button_view.pack(side=LEFT, padx=4, pady=10)
button_update = Button(frame_button, activebackground="#84e389", text="UPDATE", width='10', bg="light blue",
                       command=update)
button_update.pack(side=LEFT, padx=4, pady=5)
button_remove = Button(frame_button, activebackground="#84e389", text="REMOVE", width='10', bg="light blue",
                       command=remove)
button_remove.pack(side=LEFT, padx=4, pady=10)
button_find = Button(frame_button, activebackground="#84e389", text="FIND", width='10', bg="light blue", command=find)
button_find.pack(side=LEFT, padx=4, pady=10)
##----Display and scrollbar-----
listframe = Frame(root)
listframe.place(y=0)
listboxname = Listbox(listframe, width="27", height="7", font=("Courier New", 17), bg='#b7b7b7', fg="black",
                      highlightthickness=0, cursor="hand2", selectbackground="light gray", activestyle="none")
listboxname.pack(side=LEFT, fill=BOTH, padx=10, pady=10)
scroll = Scrollbar(listframe)
scroll.pack(side=LEFT, fill=BOTH)
listboxname.config(yscrollcommand=scroll.set)
initialise()
root.mainloop()