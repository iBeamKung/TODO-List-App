import tkinter as tk
from tkinter import OptionMenu, font as tkfont
from tkinter import messagebox
from tkinter.constants import *

import todolist_database
data_todo = todolist_database.database_todolist()

### https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("384x683")
        self.title("TODO List Application")
        self.iconbitmap(default='assets/list.ico')
        self.resizable(width=False, height=False)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.user_id = -1

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, FolderPage, FolderPage_add, TodoPage, TodoPage_add,FinishedPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg = tk.Canvas(self, width=296, height=216)
        self.image_bg_link = tk.PhotoImage(file="assets\Login\BG_Login.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 295, anchor='center')

        image_logo = tk.Canvas(self, width=305, height=75)
        self.image_logo_link = tk.PhotoImage(file="assets\Login\Logo.png")
        image_logo.create_image(5, 5, anchor=NW, image=self.image_logo_link)
        image_logo.place(x=192, y= 120, anchor='center')

        #label_login = tk.Label(self, text='Login', bg="blue")
        #label_login.place(x=192, y= 120, anchor='center')

        label_username = tk.Label(self, text='Username:', bg="white",font=("Calibri 12"))
        label_username.place(x=130, y= 250, anchor='e')

        input_username = tk.StringVar()
        entry_username = tk.Entry(self,textvariable=input_username,width=20,borderwidth=2,font=("Calibri 13"))
        entry_username.place(x=222, y= 250 ,anchor='center')

        label_password = tk.Label(self, text='Password:', bg="white",font=("Calibri 12"))
        label_password.place(x=130, y= 300, anchor='e')

        input_password = tk.StringVar()
        entry_password = tk.Entry(self,textvariable=input_password,show="*",width=20,borderwidth=2,font=("Calibri 13"))
        entry_password.place(x=222, y= 300 ,anchor='center')

        button_login = tk.Button(self, text="Login",
                            command=lambda:  self.check(input_username,input_password) )
        button_login.place(x=192, y= 350 ,anchor='center')

    def check(self,username,password) :
        id = -1
        input_username = username.get() 
        input_password = password.get()
        print("input_username : ",input_username , "\ninput_password : " , input_password )
        client_username = data_todo.username()
        client_password = data_todo.password()
        for i in range(len(client_username)) :
            if (client_username[i] == input_username and client_password[i] == input_password ) :
                self.controller.show_frame("FolderPage")
                id = i
        print(id)
        if id > -1:
            self.controller.user_id = id
            self.controller.frames["FolderPage"].update_listbox()
            print("user_ID :",self.controller.user_id)
            return id
        else:
            tk.messagebox.showerror("Error", "incorrect username or password")

class FolderPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg = tk.Canvas(self, width=356, height=576)
        self.image_bg_link = tk.PhotoImage(file="assets/folder/bg.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 375, anchor='center')

        image_logo = tk.Canvas(self, width=43, height=30)
        self.image_logo_link = tk.PhotoImage(file="assets/folder/folder.png")
        image_logo.create_image(2, 2, anchor=NW, image=self.image_logo_link)
        image_logo.place(x=49, y= 49, anchor='center')

        self.label_todo = tk.Label(self, text="TO-DO Folder", bg = "#f2f1f6", font=("Calibri 20 bold"))
        self.label_todo.place(x=70, y= 73, anchor='sw')


        self.image_btn_add_link = tk.PhotoImage(file='assets/folder/add.png')
        image_btn_add_label = tk.Label(self,image=self.image_btn_add_link)
        image_btn_add = tk.Button(self, image=self.image_btn_add_link,borderwidth=0,command=lambda: self.addFolder())
        image_btn_add.place(x=295, y= 50, anchor='center')

        self.image_btn_del_link = tk.PhotoImage(file='assets/folder/del.png')
        image_btn_del_label = tk.Label(self,image=self.image_btn_del_link)
        image_btn_del = tk.Button(self, image=self.image_btn_del_link,borderwidth=0,command=lambda: self.delFolder(self.listbox.curselection()))
        image_btn_del.place(x=340, y= 50, anchor='center')

        self.listbox = tk.Listbox(self,bd=0,font=("Calibri 23 bold"),highlightthickness=0,activestyle='none')
        self.listbox.place(x=190, y= 370, anchor='center',width=300, height=545)

        self.listbox.bind('<Double-Button>', lambda x: self.select_folder(self.listbox.selection_get()[1:]))

        scrollbar = tk.Scrollbar(self)
        self.update_listbox()

        self.listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = self.listbox.yview)

    def update_listbox(self):
        print("Update Folder !")
        self.listbox.delete(0,END)
        name_folder = data_todo.folder(self.controller.user_id)
        for values in name_folder:
            self.listbox.insert(END,"📁"+ values)

    def select_folder(self,selectedFolder):
        print("Select Folder :", selectedFolder)
        self.controller.frames["TodoPage"].label_todo.config(text = selectedFolder)
        self.controller.frames["TodoPage"].update_listbox()
        self.controller.show_frame("TodoPage")

    def addFolder(self):
        print("Folder Add Page !!!")
        self.controller.show_frame("FolderPage_add")

    def delFolder(self,nameFolder):
        if(nameFolder != ()):
            print("Delete Folder :", self.listbox.get(nameFolder[0]))
            data_todo.del_folder(self.controller.user_id,self.listbox.get(nameFolder[0])[1:])
            self.listbox.delete(nameFolder[0])
        else:
            print("Delete Folder Error !")
            tk.messagebox.showerror("Error", "Error : No Folder Select")

class FolderPage_add(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg = tk.Canvas(self, width=356, height=264)
        self.image_bg_link = tk.PhotoImage(file="assets/folder/bg_add.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 342, anchor='center')

        image_logo = tk.Canvas(self, width=43, height=30)
        self.image_logo_link = tk.PhotoImage(file="assets/folder/folder.png")
        image_logo.create_image(2, 2, anchor=NW, image=self.image_logo_link)
        image_logo.place(x=49, y= 190, anchor='center')

        self.label_todo = tk.Label(self, text="Add Folder", bg = "#f2f1f6", font=("Calibri 22 bold"))
        self.label_todo.place(x=70, y= 210, anchor='sw')

        self.image_btn_back_link = tk.PhotoImage(file='assets/folder/x.png')
        image_btn_back = tk.Button(self, image=self.image_btn_back_link,borderwidth=0,command=lambda: self.controller.show_frame("FolderPage"))
        image_btn_back.place(x=340, y= 190, anchor='center')

        label_nameFolder = tk.Label(self, text='Name Folder :', bg="white",font=("Calibri 14"))
        label_nameFolder.place(x=165, y= 300, anchor='e')

        input_nameFolder = tk.StringVar()
        entry_nameFolder = tk.Entry(self,textvariable=input_nameFolder,width=30,borderwidth=2,font=("Calibri 13"))
        entry_nameFolder.place(x=192, y= 325 ,anchor='center')

        self.image_btn_submit_link = tk.PhotoImage(file='assets/folder/btn_sub.png')
        image_btn_submit = tk.Button(self, image=self.image_btn_submit_link,borderwidth=0,command=lambda: [self.add(input_nameFolder.get()), entry_nameFolder.delete(0, 'end')])
        image_btn_submit.place(x=192, y= 432, anchor='center')

    def add(self,input_name):
        print("Add Folder :",input_name)
        data_todo.add_folder(self.controller.user_id,input_name)
        self.controller.frames["FolderPage"].update_listbox()
        self.controller.show_frame("FolderPage")

class TodoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg = tk.Canvas(self, width=356, height=576)
        self.image_bg_link = tk.PhotoImage(file="assets/todo/bg.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 375, anchor='center')

        self.image_logo_link = tk.PhotoImage(file='assets/todo/list.png')
        image_logo_label = tk.Label(self,image=self.image_logo_link)
        image_logo_add = tk.Button(self, image=self.image_logo_link,borderwidth=0,command=lambda: controller.show_frame("FolderPage"))
        image_logo_add.place(x=49, y= 49, anchor='center')

        self.label_todo = tk.Label(self, text="", bg = "#f2f1f6", font=("Calibri 22 bold"))
        self.label_todo.place(x=75, y= 73, anchor='sw')

        self.listbox = tk.Listbox(self,bd=0,font=("Calibri 18"),highlightthickness=0,activestyle='none')
        self.listbox.place(x=190, y= 370, anchor='center',width=300, height=545)
        scrollbar = tk.Scrollbar(self)
        for values in range(3):
            self.listbox.insert(END, values)
        self.listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = self.listbox.yview)

        self.image_btn_done_link = tk.PhotoImage(file='assets/todo/done.png')
        image_btn_done_label = tk.Label(self,image=self.image_btn_done_link)
        image_btn_done_add = tk.Button(self, image=self.image_btn_done_link,borderwidth=0,command=lambda: self.doneTodo(self.label_todo.cget("text"),self.listbox.curselection()))
        image_btn_done_add.place(x=277, y= 53, anchor='center')

        self.image_btn_add_link = tk.PhotoImage(file='assets/todo/add.png')
        image_btn_add_label = tk.Label(self,image=self.image_btn_add_link)
        image_btn_add = tk.Button(self, image=self.image_btn_add_link,borderwidth=0,command=lambda: self.addTodo())
        image_btn_add.place(x=312, y= 53, anchor='center')

        self.image_btn_del_link = tk.PhotoImage(file='assets/todo/del.png')
        image_btn_del_label = tk.Label(self,image=self.image_btn_del_link)
        image_btn_del = tk.Button(self, image=self.image_btn_del_link,borderwidth=0,command=lambda: self.delTodo(self.label_todo.cget("text"),self.listbox.curselection()))
        image_btn_del.place(x=347, y= 53, anchor='center')

        button_finished = tk.Button(self, text = "Finished" ,command=lambda: controller.show_frame("FinishedPage"))
        button_finished.place(x=192, y= 53 ,anchor='center')

    def update_listbox(self):
        print("Update TO-DO List :",self.label_todo.cget("text"))
        self.listbox.delete(0,END)
        name_task = data_todo.display_task(self.controller.user_id,self.label_todo.cget("text"))
        for values in name_task:
            self.listbox.insert(END,values)
            
    def addTodo(self):
        print("TO-DO Add Page !!!")
        self.controller.show_frame("TodoPage_add")

    def doneTodo(self,in_Folder,in_Todo):
        if(in_Todo != ()):
            print("Done TO-DO List :", self.listbox.get(in_Todo[0]))
            data_todo.del_task(in_Folder,in_Todo[0])
            self.listbox.delete(in_Todo[0])
        else:
            tk.messagebox.showerror("Error", "Error : No TO-DO Select")

    def delTodo(self,in_Folder,in_Todo):
        if(in_Todo != ()):
            print("Delete TO-DO List :", self.listbox.get(in_Todo[0]))
            print(in_Folder,in_Todo)
            data_todo.del_task(self.controller.user_id,in_Folder,in_Todo[0])
            self.listbox.delete(in_Todo[0])
        else:
            tk.messagebox.showerror("Error", "Error : No TO-DO Select")

class TodoPage_add(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg = tk.Canvas(self, width=356, height=264)
        self.image_bg_link = tk.PhotoImage(file="assets/folder/bg_add.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 342, anchor='center')

        image_logo = tk.Canvas(self, width=43, height=30)
        self.image_logo_link = tk.PhotoImage(file="assets/todo/list.png")
        image_logo.create_image(2, 2, anchor=NW, image=self.image_logo_link)
        image_logo.place(x=49, y= 190, anchor='center')

        self.label_todo = tk.Label(self, text="Add TO-DO", bg = "#f2f1f6", font=("Calibri 22 bold"))
        self.label_todo.place(x=70, y= 210, anchor='sw')

        self.image_btn_back_link = tk.PhotoImage(file='assets/folder/x.png')
        image_btn_back = tk.Button(self, image=self.image_btn_back_link,borderwidth=0,command=lambda: self.controller.show_frame("TodoPage"))
        image_btn_back.place(x=340, y= 190, anchor='center')

        label_nameTodo = tk.Label(self, text='TO-DO :', bg="white",font=("Calibri 14"))
        label_nameTodo.place(x=50, y= 240, anchor='w')

        input_nameTodo = tk.StringVar()
        entry_nameTodo = tk.Entry(self,textvariable=input_nameTodo,width=30,borderwidth=2,font=("Calibri 13"))
        entry_nameTodo.place(x=192, y= 265 ,anchor='center')

        self.image_btn_submit_link = tk.PhotoImage(file='assets/folder/btn_sub.png')
        image_btn_submit = tk.Button(self, image=self.image_btn_submit_link,borderwidth=0,command=lambda: [self.add(self.controller.frames["TodoPage"].label_todo.cget("text"),input_nameDate.get(),input_nameHour.get()+":"+input_nameMinute.get(),input_nameTodo.get()), entry_nameTodo.delete(0, 'end')])
        image_btn_submit.place(x=192, y= 432, anchor='center')

        hours_list = []
        for i in range(24) :
            hours_list.append(i)
        minute_list = []
        for i in range(60) :
            minute_list.append(i) 

        label_nameHour = tk.Label(self, text='Hour :', bg="white",font=("Calibri 14"))
        label_nameHour.place(x=50, y= 300, anchor='w')

        input_nameHour = tk.StringVar()
        entry_nameHour = tk.Entry(self,textvariable=input_nameHour,width=8,borderwidth=2,font=("Calibri 13"))
        entry_nameHour.place(x=142, y= 300 ,anchor='center')

        label_nameMinute = tk.Label(self, text='Minute :', bg="white",font=("Calibri 14"))
        label_nameMinute.place(x=180, y= 300, anchor='w')

        input_nameMinute = tk.StringVar()
        entry_nameMinute = tk.Entry(self,textvariable=input_nameMinute,width=8,borderwidth=2,font=("Calibri 13"))
        entry_nameMinute.place(x=290, y= 300 ,anchor='center')

        label_nameDate = tk.Label(self, text='Date : Ex 01/01/2022', bg="white",font=("Calibri 14"))
        label_nameDate.place(x=50, y= 340, anchor='w')

        input_nameDate = tk.StringVar()
        entry_nameDate = tk.Entry(self,textvariable=input_nameDate,width=30,borderwidth=2,font=("Calibri 13"))
        entry_nameDate.place(x=192, y= 370 ,anchor='center')

    def add(self,input_nameFolder,input_date,input_time,input_task): #user_ID,in_folderName,in_date,in_time,in_task
        print("Add TO-DO List :",input_task)
        data_todo.add_task(self.controller.user_id,input_nameFolder,input_date,input_time,input_task)
        self.controller.frames["TodoPage"].update_listbox()
        self.controller.show_frame("TodoPage")

class FinishedPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg = tk.Canvas(self, width=356, height=576)
        self.image_bg_link = tk.PhotoImage(file="assets/todo/bg.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 375, anchor='center')

        button_finished = tk.Button(self, text = "back" ,command=lambda: controller.show_frame("TodoPage"))
        button_finished.place(x=49, y= 49 ,anchor='center')

        self.label_todo = tk.Label(self, text="", bg = "#f2f1f6", font=("Calibri 22 bold"))
        self.label_todo.place(x=75, y= 73, anchor='sw')

        self.listbox = tk.Listbox(self,bd=0,font=("Calibri 18"),highlightthickness=0,activestyle='none')
        self.listbox.place(x=190, y= 370, anchor='center',width=300, height=545)
        scrollbar = tk.Scrollbar(self)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()