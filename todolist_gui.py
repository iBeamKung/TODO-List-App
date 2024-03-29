import tkinter as tk
from tkinter import OptionMenu, font as tkfont
from tkinter import messagebox
from tkinter import filedialog
from tkinter.constants import *

from tkcalendar import Calendar

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

import os

import todolist_database
#data_todo = todolist_database.database_todolist()

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
        
        self.data_todo = todolist_database.database_todolist()

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        """ Load All Page into Mainapp"""
        self.frames = {}
        for F in (LoginPage,RegisterPage, LoadPage, FolderPage, FolderPage_add, StatFolderPage, TodoPage, TodoPage_add,TodoPage_finished, StatTodoPage):
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
        self.image_bg_link = tk.PhotoImage(file="assets\login\BG_Login.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 341, anchor='center')

        image_logo = tk.Canvas(self, width=169, height=70)
        self.image_logo_link = tk.PhotoImage(file="assets\login\logo.png")
        image_logo.create_image(4, 4, anchor=NW, image=self.image_logo_link)
        image_logo.place(x=192, y= 170, anchor='center')

        label_username = tk.Label(self, text='Username:', bg="white",font=("Calibri 12"))
        label_username.place(x=130, y= 296, anchor='e')

        input_username = tk.StringVar()
        entry_username = tk.Entry(self,textvariable=input_username,width=20,borderwidth=2,font=("Calibri 13"))
        entry_username.place(x=222, y= 296 ,anchor='center')

        label_password = tk.Label(self, text='Password:', bg="white",font=("Calibri 12"))
        label_password.place(x=130, y= 346, anchor='e')

        input_password = tk.StringVar()
        entry_password = tk.Entry(self,textvariable=input_password,show="*",width=20,borderwidth=2,font=("Calibri 13"))
        entry_password.place(x=222, y= 346 ,anchor='center')

        button_login = tk.Button(self, text="Login",command=lambda: [
                                                                        self.check(input_username.get(),input_password.get()),
                                                                        entry_username.delete(0, 'end'),
                                                                        entry_password.delete(0, 'end')
                                                                    ]
                                )
        button_login.place(x=192, y= 396 ,anchor='center')

        button_register = tk.Button(self, text="Register", command=lambda: self.controller.show_frame("RegisterPage"))
        button_register.place(x=286, y= 396 ,anchor='center')

    def check(self,username,password) :
        print("GUI :", "Login", "Username>", username, "Password>", password)
        user_id = self.controller.data_todo.loginCheck(username,password)
        if user_id == "error":
            print("GUI : Login Failed")
            tk.messagebox.showerror("Error", "incorrect username or password")
        else:
            print("GUI :", "Login Success !", "user_ID>", user_id)
            self.controller.user_id = user_id
            self.controller.frames["FolderPage"].update_listbox()
            self.controller.show_frame("FolderPage")

class RegisterPage(tk.Frame) :

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg = tk.Canvas(self, width=356, height=264)
        self.image_bg_link = tk.PhotoImage(file="assets/folder/bg_add.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 342, anchor='center')

        self.label_todo = tk.Label(self, text="Add User", bg = "#f2f1f6", font=("Calibri 22 bold"))
        self.label_todo.place(x=30, y= 210, anchor='sw')

        self.image_btn_back_link = tk.PhotoImage(file='assets/folder/x.png')
        image_btn_back = tk.Button(self, image=self.image_btn_back_link,borderwidth=0,command=lambda: self.controller.show_frame("LoginPage"))
        image_btn_back.place(x=340, y= 190, anchor='center')

        label_newUsername = tk.Label(self, text='New username :', bg="white",font=("Calibri 14"))
        label_newUsername.place(x=180, y= 250, anchor='e')

        input_newUsername = tk.StringVar()
        self.entry_newUsername = tk.Entry(self,textvariable=input_newUsername,width=30,borderwidth=2,font=("Calibri 13"))
        self.entry_newUsername.place(x=192, y= 285 ,anchor='center')

        label_newPassword = tk.Label(self, text='New password :' , bg="white",font=("Calibri 14"))
        label_newPassword.place(x=180, y= 320, anchor='e')

        input_newPassword = tk.StringVar()
        self.entry_newPassword = tk.Entry(self,textvariable=input_newPassword,show="*",width=30,borderwidth=2,font=("Calibri 13"))
        self.entry_newPassword.place(x=192, y= 355 ,anchor='center')

        button_create = tk.Button(self, text="create", command=lambda: self.create_account(input_newUsername.get(),input_newPassword.get()))
        button_create.place(x=192, y= 412, anchor='center')

    def create_account(self,newUsername,newPassword) :
        print("GUI :", "Register", "Username>", newUsername, "Password>", newPassword)
        if(self.controller.data_todo.register_user(newUsername.lower(),newPassword)):
            print("GUI :", "Register Success !", "Username>", newUsername)
            self.entry_newUsername.delete(0, 'end')
            self.entry_newPassword.delete(0, 'end')
            self.controller.show_frame("LoginPage")
            tk.messagebox.showinfo("Register", "Congratulations, your account has been successfully created.")
        else:
            print("GUI : Register Failed")
            tk.messagebox.showerror("Error", "Error : Username is already taken")

class LoadPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg = tk.Canvas(self, width=356, height=264)
        self.image_bg_link = tk.PhotoImage(file="assets/folder/bg_add.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 342, anchor='center')

        image_logo = tk.Canvas(self, width=43, height=30)
        self.image_logo_link = tk.PhotoImage(file="assets/folder/folder1.png")
        image_logo.create_image(2, 2, anchor=NW, image=self.image_logo_link)
        image_logo.place(x=49, y= 190, anchor='center')

        self.label_todo = tk.Label(self, text="Import / Export TODO", bg = "#f2f1f6", font=("Calibri 18 bold"))
        self.label_todo.place(x=70, y= 210, anchor='sw')

        self.image_btn_back_link = tk.PhotoImage(file='assets/folder/x.png')
        image_btn_back = tk.Button(self, image=self.image_btn_back_link,borderwidth=0,command=lambda: self.controller.show_frame("FolderPage"))
        image_btn_back.place(x=340, y= 190, anchor='center')

        self.image_btn_export_link = tk.PhotoImage(file='assets/load/export.png')
        image_btn_export = tk.Button(self, image=self.image_btn_export_link,borderwidth=0,highlightthickness=0,command=lambda: self.export_data())
        image_btn_export.place(x=192, y= 292, anchor='center')

        self.image_btn_import_link = tk.PhotoImage(file='assets/load/import.png')
        image_btn_import = tk.Button(self, image=self.image_btn_import_link,borderwidth=0,highlightthickness=0,command=lambda: self.import_data())
        image_btn_import.place(x=192, y= 368, anchor='center')

    def import_data(self):
        """ Search JSON file to import """
        print("GUI :", "Import Data !")
        file = filedialog.askopenfile(mode='r', filetypes=[('JSON Files', '*.json')])
        if file:
            import_confirm = tk.messagebox.askyesno("Import Data","Are your sure you want to Import this data ?")
            if import_confirm:
                filepath = os.path.abspath(file.name)
                self.controller.data_todo.import_data(self.controller.user_id,filepath)
                tk.messagebox.showinfo("Import Data", "Import Data Success!")
                self.controller.frames["FolderPage"].update_listbox()
                self.controller.show_frame("FolderPage")

    def export_data(self):
        """ Get Folder to Export JSON file """
        print("GUI :", "Export Data !")
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.controller.data_todo.export_data(self.controller.user_id,folder_selected)
            tk.messagebox.showinfo("Export Data", "Export Data Success! : " + folder_selected)
            self.controller.show_frame("FolderPage")


class FolderPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg = tk.Canvas(self, width=356, height=491)
        self.image_bg_link = tk.PhotoImage(file="assets/folder/bg1.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 332, anchor='center')

        image_logo = tk.Canvas(self, width=43, height=30)
        self.image_logo_link = tk.PhotoImage(file="assets/folder/folder1.png")
        image_logo.create_image(2, 2, anchor=NW, image=self.image_logo_link)
        image_logo.place(x=49, y= 49, anchor='center')

        self.label_todo = tk.Label(self, text="Category", bg = "#f2f1f6", font=("Calibri 22 bold"))
        self.label_todo.place(x=70, y= 73, anchor='sw')


        self.image_btn_load_link = tk.PhotoImage(file='assets/folder/load.png')
        image_btn_load = tk.Button(self, image=self.image_btn_load_link,borderwidth=0,command=lambda: self.controller.show_frame("LoadPage"))
        image_btn_load.place(x=240, y= 53, anchor='center')

        self.image_btn_add_link = tk.PhotoImage(file='assets/folder/add.png')
        image_btn_add = tk.Button(self, image=self.image_btn_add_link,borderwidth=0,command=lambda: self.addFolder())
        image_btn_add.place(x=275, y= 53, anchor='center')

        self.image_btn_del_link = tk.PhotoImage(file='assets/folder/del.png')
        image_btn_del = tk.Button(self, image=self.image_btn_del_link,borderwidth=0,command=lambda: self.delFolder(self.listbox.curselection()))
        image_btn_del.place(x=310, y= 53, anchor='center')

        self.image_btn_logout_link = tk.PhotoImage(file='assets/folder/logout.png')
        image_btn_logout = tk.Button(self, image=self.image_btn_logout_link,borderwidth=0,command=lambda: self.logout())
        image_btn_logout.place(x=345, y= 53, anchor='center')

        self.listbox = tk.Listbox(self,bd=0,font=("Calibri 20 bold"),highlightthickness=0,activestyle='none')
        self.listbox.place(x=190, y= 332, anchor='center',width=300, height=460)

        self.listbox.bind('<Double-Button>', lambda x: self.select_folder(self.listbox.selection_get()[1:]))

        scrollbar = tk.Scrollbar(self)

        self.listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = self.listbox.yview)

        image_bg2 = tk.Canvas(self, width=356, height=75)
        self.image_bg2_link = tk.PhotoImage(file="assets/folder/bg2.png")
        image_bg2.create_image(0, 0, anchor=NW, image=self.image_bg2_link)
        image_bg2.place(x=192, y= 625, anchor='center')

        self.image_btn_stat_link = tk.PhotoImage(file='assets/folder/stat.png')
        image_btn_stat = tk.Button(self, image=self.image_btn_stat_link,borderwidth=0,highlightthickness=0,command=lambda: [
                                                                                                                                self.controller.show_frame("StatFolderPage"),
                                                                                                                                self.controller.frames["StatFolderPage"].pieChartFol(),
                                                                                                                                self.controller.frames["StatFolderPage"].barChartFol()
                                                                                                                            ]
                                   )
        image_btn_stat.place(x=54, y= 620, anchor='center')

        self.label_all_stat = tk.Label(self, text="AllTask:", bg = "#ffffff", font=("Calibri 13 bold"))
        self.label_all_stat.place(x=80, y= 632, anchor='sw')

        self.label_done_stat = tk.Label(self, text="Done:", bg = "#ffffff", font=("Calibri 13  bold"))
        self.label_done_stat.place(x=182, y= 632, anchor='sw')

        self.label_undone_stat = tk.Label(self, text="Undone:", bg = "#ffffff", font=("Calibri 13 bold"))
        self.label_undone_stat.place(x=260, y= 632, anchor='sw')

    def update_listbox(self):
        """ Refresh Page """
        print("GUI :", "Update FolderPage !")
        self.listbox.delete(0,END)
        name_folder = self.controller.data_todo.folder(self.controller.user_id)
        for values in name_folder:
            self.listbox.insert(END,"📁"+ values)
        stat = self.controller.data_todo.display_all_stat(self.controller.user_id)
        self.label_all_stat.config(text = "AllTask: "+ str(stat[0]))
        self.label_done_stat.config(text = "Done: "+ str(stat[1]))
        self.label_undone_stat.config(text = "Undone: "+ str(stat[2]))

    def select_folder(self,selectedFolder):
        print("GUI :", "Select Folder >", selectedFolder)
        self.controller.frames["TodoPage"].label_todo.config(text = selectedFolder)
        self.controller.frames["TodoPage"].update_listbox()
        self.controller.frames["TodoPage_finished"].label_todo.config(text = selectedFolder)
        self.controller.frames["TodoPage_finished"].update_listbox()
        self.controller.show_frame("TodoPage")

    def addFolder(self):
        print("GUI :", "Folder Add Page !")
        self.controller.show_frame("FolderPage_add")

    def delFolder(self,nameFolder):
        if(nameFolder != ()):
            print("GUI :", "Delete Folder",self.listbox.get(nameFolder[0]))
            delete_confirm = tk.messagebox.askyesno("Delete Folder","Would you like to delete the "+self.listbox.get(nameFolder[0])+'?')
            if delete_confirm:
                print("Delete Folder :", self.listbox.get(nameFolder[0]))
                self.controller.data_todo.del_folder(self.controller.user_id,self.listbox.get(nameFolder[0])[1:])
                self.update_listbox()
        else:
            print("GUI :", "Delete Folder Error !")
            tk.messagebox.showerror("Error", "Error : No Folder Select")
    
    def logout(self):
        print("GUI :", "Logout !")
        logout_confirm = tk.messagebox.askyesno("Logout","Are your sure you want to Logout?")
        if logout_confirm:
            self.controller.show_frame("LoginPage")

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
        self.image_logo_link = tk.PhotoImage(file="assets/folder/folder1.png")
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
        image_btn_submit = tk.Button(self, image=self.image_btn_submit_link,borderwidth=0,command=lambda: [
                                                                                                            self.add(input_nameFolder.get()),
                                                                                                            entry_nameFolder.delete(0, 'end')
                                                                                                          ]
                                    )
        image_btn_submit.place(x=192, y= 432, anchor='center')

    def add(self,input_name):
        print("GUI :", "Add Folder", "Folder>", input_name)
        if input_name != "":
            if(self.controller.data_todo.add_folder(self.controller.user_id,input_name) == "error"):
                tk.messagebox.showerror("Error", "Error : Foldername is already taken")
            else:
                self.controller.show_frame("FolderPage")
                self.controller.frames["FolderPage"].update_listbox()
        else:
            tk.messagebox.showerror("Error", "Error : Foldername is None")
        
class StatFolderPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg = tk.Canvas(self, width=356, height=576)
        self.image_bg_link = tk.PhotoImage(file="assets/stat/bg_test.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 299, anchor='center')

        self.label_alltask = tk.Label(self, text="All Task", bg = "#ffffff", font=("Calibri 22 bold"))
        self.label_alltask.place(x=40, y= 300, anchor='sw')

        self.image_btn_back_link = tk.PhotoImage(file='assets/stat/back.png')
        image_btn_back = tk.Button(self, image=self.image_btn_back_link,borderwidth=0,command=lambda: [self.controller.show_frame("FolderPage")])
        image_btn_back.place(x=192, y= 631, anchor='center')

    def pieChartFol(self):
        data_stat = self.controller.data_todo.statGraphFol(self.controller.user_id)
        #['']
        fig1 = Figure(figsize=(3, 2.5)) # create a figure object
        ax = fig1.add_subplot(111) # add an Axes to the figure

        ax.pie(data_stat[1], labels=data_stat[0],autopct='%0.1f%%', startangle=90)

        pieChart = FigureCanvasTkAgg(fig1,self)
        pieChart.get_tk_widget().place(x=192, y= 40, anchor='n')

        self.label_category = tk.Label(self, text="Category", bg = "#ffffff", font=("Calibri 22 bold"))
        self.label_category.place(x=40, y= 73, anchor='sw')

    def barChartFol(self):
        data_stat = self.controller.data_todo.statGraphFol(self.controller.user_id)

        x = np.arange(len(data_stat[0]))  # the label locations [0,1]
        width = 0.2  # the width of the bars

        fig2 = Figure(figsize=(3,2.5), dpi=100)
        barChart = fig2.add_subplot(111)

        barChart.bar(x - width, data_stat[1], width, label='Task',color = "#8e44ad")
        barChart.bar(x, data_stat[2], width, label='Complete',color = "#2ecc71")
        barChart.bar(x + width, data_stat[3], width, label='Incomplete',color= "#e74c3c")

        barChart.set_xticks(x)
        barChart.set_xticklabels(data_stat[0], rotation='vertical', fontsize=10)
        barChart.legend()
        barChart.spines["top"].set_visible(False)
        barChart.spines["right"].set_visible(False)
        barChart.spines["left"].set_visible(False)
        fig2.tight_layout()

        for bar in barChart.patches:
            bar_value = bar.get_height()
            text = f'{bar_value:,}'
            text_x = bar.get_x() + bar.get_width() / 2
            text_y = bar.get_y() + bar_value
            bar_color = bar.get_facecolor()
            barChart.text(text_x, text_y, text, ha='center', va='bottom', color=bar_color,size=8)

        barDisplay = FigureCanvasTkAgg(fig2, self)
        barDisplay.get_tk_widget().place(x=192, y= 290, anchor='n')

        self.label_alltask = tk.Label(self, text="All Task", bg = "#ffffff", font=("Calibri 22 bold"))
        self.label_alltask.place(x=40, y= 300, anchor='sw')

class TodoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg1 = tk.Canvas(self, width=356, height=491)
        self.image_bg1_link = tk.PhotoImage(file="assets/todo/bg1.png")
        image_bg1.create_image(0, 0, anchor=NW, image=self.image_bg1_link)
        image_bg1.place(x=192, y= 332, anchor='center')

        self.image_logo_link = tk.PhotoImage(file='assets/todo/list.png')
        image_logo_add = tk.Button(self, image=self.image_logo_link,borderwidth=0,command=lambda: controller.show_frame("FolderPage"))
        image_logo_add.place(x=49, y= 49, anchor='center')

        self.label_todo = tk.Label(self, text="", bg = "#f2f1f6", font=("Calibri 22 bold"))
        self.label_todo.place(x=75, y= 73, anchor='sw')

        self.listbox = tk.Listbox(self,bd=0,font=("Calibri 16"),highlightthickness=0,activestyle='none')
        self.listbox.place(x=190, y= 332, anchor='center',width=300, height=460)
        scrollbar = tk.Scrollbar(self)
        self.listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = self.listbox.yview)

        self.image_btn_done_link = tk.PhotoImage(file='assets/todo/done.png')
        image_btn_done_add = tk.Button(self, image=self.image_btn_done_link,borderwidth=0,command=lambda: self.doneTodo(self.label_todo.cget("text"),self.listbox.curselection()))
        image_btn_done_add.place(x=275, y= 53, anchor='center')

        self.image_btn_add_link = tk.PhotoImage(file='assets/todo/add.png')
        image_btn_add = tk.Button(self, image=self.image_btn_add_link,borderwidth=0,command=lambda: self.addTodo())
        image_btn_add.place(x=310, y= 53, anchor='center')

        self.image_btn_del_link = tk.PhotoImage(file='assets/todo/del.png')
        image_btn_del = tk.Button(self, image=self.image_btn_del_link,borderwidth=0,command=lambda: self.delTodo(self.label_todo.cget("text"),self.listbox.curselection()))
        image_btn_del.place(x=345, y= 53, anchor='center')

        button_finished = tk.Button(self, text = "Complete" ,command=lambda: controller.show_frame("TodoPage_finished"))
        button_finished.place(x=252, y= 64 ,anchor='se')

        image_bg2 = tk.Canvas(self, width=356, height=75)
        self.image_bg2_link = tk.PhotoImage(file="assets/todo/bg2.png")
        image_bg2.create_image(0, 0, anchor=NW, image=self.image_bg2_link)
        image_bg2.place(x=192, y= 625, anchor='center')

        self.image_btn_stat_link = tk.PhotoImage(file='assets/folder/stat.png')
        image_btn_stat = tk.Button(self, image=self.image_btn_stat_link,borderwidth=0,highlightthickness=0,command=lambda: [
                                                                                                                                self.controller.show_frame("StatTodoPage"),
                                                                                                                                self.controller.frames["StatTodoPage"].pieChartFol(),
                                                                                                                                self.controller.frames["StatTodoPage"].barChartFol()
                                                                                                                            ]
                                   )
        image_btn_stat.place(x=54, y= 620, anchor='center')

        self.label_all_stat = tk.Label(self, text="FolderTask:", bg = "#ffffff", font=("Calibri 13 bold"))
        self.label_all_stat.place(x=80, y= 632, anchor='sw')

        self.label_done_stat = tk.Label(self, text="Done:", bg = "#ffffff", font=("Calibri 13  bold"))
        self.label_done_stat.place(x=182, y= 632, anchor='sw')

        self.label_undone_stat = tk.Label(self, text="Undone:", bg = "#ffffff", font=("Calibri 13 bold"))
        self.label_undone_stat.place(x=260, y= 632, anchor='sw')

    def update_listbox(self):
        print("GUI :", "Update TodoPage ! >", self.label_todo.cget("text"))
        self.listbox.delete(0,END)
        name_task = self.controller.data_todo.display_undone_task(self.controller.user_id,self.label_todo.cget("text"))
        for values in name_task:
            self.listbox.insert(END,values)
        stat = self.controller.data_todo.display_fol_stat(self.controller.user_id,self.label_todo.cget("text"))
        self.label_all_stat.config(text = "FolderTask: "+ str(stat[0]))
        self.label_done_stat.config(text = "Done: "+ str(stat[1]))
        self.label_undone_stat.config(text = "Undone: "+ str(stat[2]))

    def addTodo(self):
        print("GUI :", "Todo Add Page !")
        self.controller.show_frame("TodoPage_add")

    def doneTodo(self,in_Folder,in_Todo):
        """ get list todo to set done"""
        if(in_Todo != ()):
            for i in range(in_Todo[0]-1,-1,-1):
                if(self.listbox.get(i)[0:4] == "Date"):
                    date = self.listbox.get(i)[7:15]
                    break
            time = self.listbox.get(in_Todo[0])[0:5]
            data = self.listbox.get(in_Todo[0])[8:]
            self.controller.data_todo.done_task(self.controller.user_id,in_Folder,date,time,data)
            self.update_listbox()
            self.controller.frames["TodoPage_finished"].update_listbox()
            self.controller.frames["FolderPage"].update_listbox()
        else:
            tk.messagebox.showerror("Error", "Error : No TO-DO Select")

    def delTodo(self,in_Folder,in_Todo):
        if(in_Todo != ()):
            for i in range(in_Todo[0]-1,-1,-1):
                if(self.listbox.get(i)[0:4] == "Date"):
                    date = self.listbox.get(i)[7:15]
                    break
            time = self.listbox.get(in_Todo[0])[0:5]
            data = self.listbox.get(in_Todo[0])[8:]
            if(time[2] == ":"):
                delete_confirm = tk.messagebox.askyesno("Delete TODO","Would you like to delete the '"+data+"'?")
                if delete_confirm:
                    self.controller.data_todo.del_task(self.controller.user_id,in_Folder,date,time,data)
                    self.update_listbox()
                    self.controller.frames["TodoPage_finished"].update_listbox()
                    self.controller.frames["FolderPage"].update_listbox()
            else:
                return 0
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

        label_nameHour = tk.Label(self, text='Hour :', bg="white",font=("Calibri 14"))
        label_nameHour.place(x=50, y= 300, anchor='w')

        input_nameHour = tk.StringVar()
        hours = ('00', '01', '02', '03', '04', '05', '06', '07',
                '08', '09', '10', '11', '12', '13', '14', '15',
                '16', '17', '18', '19', '20', '21', '22', '23', '24'
                )
        input_nameHour.set(hours[0])

        hrs = OptionMenu(self, input_nameHour, *hours)
        hrs.place(x=142, y= 300 ,anchor='center')

        input_nameMinute = tk.StringVar()
        minutes = ('00', '01', '02', '03', '04', '05', '06', '07',
                '08', '09', '10', '11', '12', '13', '14', '15',
                '16', '17', '18', '19', '20', '21', '22', '23',
                '24', '25', '26', '27', '28', '29', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39',
                '40', '41', '42', '43', '44', '45', '46', '47',
                '48', '49', '50', '51', '52', '53', '54', '55',
                '56', '57', '58', '59')
        input_nameMinute.set(minutes[0])

        mins = OptionMenu(self, input_nameMinute, *minutes)
        mins.place(x=290, y= 300 ,anchor='center')

        label_nameMinute = tk.Label(self, text='Minute :', bg="white",font=("Calibri 14"))
        label_nameMinute.place(x=180, y= 300, anchor='w')

        label_nameDate = tk.Label(self, text='Date :', bg="white",font=("Calibri 14"))
        label_nameDate.place(x=50, y= 340, anchor='w')

        input_nameDate = tk.StringVar()
        entry_nameDate = tk.Entry(self,textvariable=input_nameDate,width=30,borderwidth=2,state=DISABLED,font=("Calibri 13"))
        entry_nameDate.place(x=192, y= 370 ,anchor='center')

        table_Data = Calendar(self, selectmode = 'day',date_pattern='dd/MM/yy',year = 2022, month = 1,day = 1)
        table_Data.place(x=192, y= 570 ,anchor='center')

        btn_getDate = tk.Button(self, text="Get Date", command=lambda: input_nameDate.set(table_Data.get_date()) )
        btn_getDate.place(x=252, y= 340 ,anchor='center')

        self.image_btn_submit_link = tk.PhotoImage(file='assets/folder/btn_sub.png')
        image_btn_submit = tk.Button(self, image=self.image_btn_submit_link,borderwidth=0,command=lambda: [
                                                                                                            self.add(
                                                                                                                     self.controller.frames["TodoPage"].label_todo.cget("text"),
                                                                                                                     input_nameDate.get(),
                                                                                                                     input_nameHour.get()+":"+input_nameMinute.get(),
                                                                                                                     input_nameTodo.get()
                                                                                                                    ),
                                                                                                            entry_nameTodo.delete(0, 'end')
                                                                                                          ]
                                     )
        image_btn_submit.place(x=192, y= 432, anchor='center')


    def add(self,input_nameFolder,input_date,input_time,input_task):
        print("GUI :", " TO-DO List", "TODO>",input_task)
        if input_date != "" and input_task != "":
            self.controller.data_todo.add_task(self.controller.user_id,input_nameFolder,input_date,input_time,input_task)
            self.controller.frames["FolderPage"].update_listbox()
            self.controller.frames["TodoPage"].update_listbox()
            self.controller.show_frame("TodoPage")
        else:
            tk.messagebox.showerror("Error", "Error : Todo Entry is None")

class TodoPage_finished(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg = tk.Canvas(self, width=356, height=576)
        self.image_bg_link = tk.PhotoImage(file="assets/todo/bg.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 375, anchor='center')

        self.image_logo_link = tk.PhotoImage(file='assets/todo/list.png')
        image_logo_add = tk.Button(self, image=self.image_logo_link,borderwidth=0,command=lambda: controller.show_frame("FolderPage"))
        image_logo_add.place(x=49, y= 49, anchor='center')

        self.label_todo = tk.Label(self, text="", bg = "#f2f1f6", font=("Calibri 22 bold"))
        self.label_todo.place(x=75, y= 73, anchor='sw')

        self.listbox = tk.Listbox(self,bd=0,font=("Calibri 16"),highlightthickness=0,activestyle='none')
        self.listbox.place(x=190, y= 370, anchor='center',width=300, height=545)
        scrollbar = tk.Scrollbar(self)
        self.listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = self.listbox.yview)

        self.image_btn_done_link = tk.PhotoImage(file='assets/todo/undone.png')
        image_btn_done_add = tk.Button(self, image=self.image_btn_done_link,borderwidth=0,command=lambda: self.undoneTodo(self.label_todo.cget("text"),self.listbox.curselection()))
        image_btn_done_add.place(x=310, y= 53, anchor='center')

        self.image_btn_del_link = tk.PhotoImage(file='assets/todo/del.png')
        image_btn_del = tk.Button(self, image=self.image_btn_del_link,borderwidth=0,command=lambda: self.delTodo(self.label_todo.cget("text"),self.listbox.curselection()))
        image_btn_del.place(x=345, y= 53, anchor='center')

        button_undone = tk.Button(self, text = "Incomplete" ,command=lambda: controller.show_frame("TodoPage"))
        button_undone.place(x=288, y= 64 ,anchor='se')

    def update_listbox(self):
        print("GUI :", "Update TodoPage Complete ! >", self.label_todo.cget("text"))
        self.listbox.delete(0,END)
        name_task = self.controller.data_todo.display_done_task(self.controller.user_id,self.label_todo.cget("text"))
        for values in name_task:
            self.listbox.insert(END,values)

    def undoneTodo(self,in_Folder,in_Todo):
        if(in_Todo != ()):
            for i in range(in_Todo[0]-1,-1,-1):
                if(self.listbox.get(i)[0:4] == "Date"):
                    date = self.listbox.get(i)[7:15]
                    break
            print("GUI :", "Todo List Undone >", self.listbox.get(in_Todo[0]))
            time = self.listbox.get(in_Todo[0])[0:5]
            data = self.listbox.get(in_Todo[0])[8:]
            self.controller.data_todo.undone_task(self.controller.user_id,in_Folder,date,time,data)
            self.update_listbox()
            self.controller.frames["TodoPage"].update_listbox()
            self.controller.frames["FolderPage"].update_listbox()
        else:
            tk.messagebox.showerror("Error", "Error : No TO-DO Select")

    def delTodo(self,in_Folder,in_Todo):
        if(in_Todo != ()):
            for i in range(in_Todo[0]-1,-1,-1):
                if(self.listbox.get(i)[0:4] == "Date"):
                    date = self.listbox.get(i)[7:15]
                    break
            time = self.listbox.get(in_Todo[0])[0:5]
            data = self.listbox.get(in_Todo[0])[8:]
            if(time[2] == ":"):
                delete_confirm = tk.messagebox.askyesno("Delete TODO","Would you like to delete the '"+data+"'?")
                if delete_confirm:
                    self.controller.data_todo.del_task(self.controller.user_id,in_Folder,date,time,data)
                    self.update_listbox()
                    self.controller.frames["TodoPage_finished"].update_listbox()
                    self.controller.frames["FolderPage"].update_listbox()
            else:
                return 0
        else:
            tk.messagebox.showerror("Error", "Error : No TO-DO Select")

class StatTodoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg = tk.Canvas(self, width=356, height=576)
        self.image_bg_link = tk.PhotoImage(file="assets/stat/bg_test.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 299, anchor='center')

        self.image_btn_back_link = tk.PhotoImage(file='assets/stat/back.png')
        image_btn_back = tk.Button(self, image=self.image_btn_back_link,borderwidth=0,command=lambda: [self.controller.show_frame("TodoPage")])
        image_btn_back.place(x=192, y= 631, anchor='center')

    def pieChartFol(self):
        data_stat = self.controller.data_todo.statGraphTodo(self.controller.user_id,self.controller.frames["TodoPage"].label_todo.cget("text"))

        fig1 = Figure(figsize=(3, 2.5)) # create a figure object
        ax = fig1.add_subplot(111) # add an Axes to the figure

        ax.pie(data_stat[1], labels=data_stat[0],autopct='%0.1f%%', startangle=90)

        pieChart = FigureCanvasTkAgg(fig1,self)
        pieChart.get_tk_widget().place(x=192, y= 40, anchor='n')

        self.label_category = tk.Label(self, text="Date", bg = "#ffffff", font=("Calibri 22 bold"))
        self.label_category.place(x=40, y= 73, anchor='sw')

    def barChartFol(self):
        data_stat = self.controller.data_todo.statGraphTodo(self.controller.user_id,self.controller.frames["TodoPage"].label_todo.cget("text"))

        x = np.arange(len(data_stat[0]))  # the label locations
        width = 0.2  # the width of the bars

        fig2 = Figure(figsize=(3,2.5), dpi=100)
        barChart = fig2.add_subplot(111)
        barChart.bar(x - width, data_stat[1], width, label='Task',color = "#8e44ad")
        barChart.bar(x, data_stat[2], width, label='Complete',color = "#2ecc71")
        barChart.bar(x + width, data_stat[3], width, label='Incomplete',color= "#e74c3c")

        barChart.set_xticks(x)
        barChart.set_xticklabels(data_stat[0], rotation='vertical', fontsize=10)
        barChart.legend()
        barChart.spines["top"].set_visible(False)
        barChart.spines["right"].set_visible(False)
        barChart.spines["left"].set_visible(False)
        fig2.tight_layout()

        for bar in barChart.patches:
            bar_value = bar.get_height()
            text = f'{bar_value:,}'
            text_x = bar.get_x() + bar.get_width() / 2
            text_y = bar.get_y() + bar_value
            bar_color = bar.get_facecolor()
            barChart.text(text_x, text_y, text, ha='center', va='bottom', color=bar_color,size=8)

        barDisplay = FigureCanvasTkAgg(fig2, self) 
        barDisplay.get_tk_widget().place(x=192, y= 290, anchor='n')

        self.label_alltask = tk.Label(self, text="Task stat", bg = "#ffffff", font=("Calibri 22 bold"))
        self.label_alltask.place(x=40, y= 300, anchor='sw')

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()