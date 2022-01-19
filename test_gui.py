import tkinter as tk
from tkinter import OptionMenu, font as tkfont
from tkinter import messagebox
from tkinter.constants import *

from tkcalendar import Calendar

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


import todolist_database
data_todo = todolist_database.database_todolist()

stockListExp = ['School' , 'Condo', 'Hospital','KFC']
stockSplitExp = [15,6,10,0]
explode = (0.05, 0.05, 0.05,0.05)

class MainApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("384x683")
        self.title("TODO List Application")
        self.iconbitmap(default='assets/list.ico')
        self.resizable(width=False, height=False)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.user_id = 0

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StatFolderPage,StatPage2):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StatFolderPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StatFolderPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')
        
        data_stat = data_todo.statFol(0)

        image_bg = tk.Canvas(self, width=356, height=576)
        self.image_bg_link = tk.PhotoImage(file="assets/stat/bg_test.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 299, anchor='center')

        self.label_alltask = tk.Label(self, text="All Task", bg = "#ffffff", font=("Calibri 22 bold"))
        self.label_alltask.place(x=40, y= 300, anchor='sw')
        
        self.image_btn_back_link = tk.PhotoImage(file='assets/stat/back.png')
        image_btn_back = tk.Button(self, image=self.image_btn_back_link,borderwidth=0,command=lambda: [self.pieChartFol(),self.barChartFol()])
        image_btn_back.place(x=192, y= 631, anchor='center')
        
    def pieChartFol(self):
        data_stat = data_todo.statFol(0)
        
        fig1 = Figure(figsize=(3, 2.5)) # create a figure object
        ax = fig1.add_subplot(111) # add an Axes to the figure
        
        ax.pie(data_stat[1], labels=data_stat[0],autopct='%0.1f%%', startangle=90)

        pieChart = FigureCanvasTkAgg(fig1,self)
        pieChart.get_tk_widget().place(x=192, y= 30, anchor='n')
        
        self.label_category = tk.Label(self, text="Category", bg = "#ffffff", font=("Calibri 22 bold"))
        self.label_category.place(x=40, y= 73, anchor='sw')
        
    def barChartFol(self):
        data_stat = data_todo.statFol(0)
        
        x = np.arange(len(data_stat[0]))  # the label locations
        width = 0.2  # the width of the bars
        
        fig2 = Figure(figsize=(3,2.5), dpi=100)
        barChart = fig2.add_subplot(111) 
        #subplot1.bar(xAxis,yAxis, color = 'lightsteelblue') 
        barChart.bar(x - width, data_stat[1], width, label='Task',color = "#8e44ad")
        barChart.bar(x, data_stat[2], width, label='Complete',color = "#2ecc71")
        barChart.bar(x + width, data_stat[3], width, label='Incomplete',color= "#e74c3c")

        #subplot1.set_ylabel('Task', fontsize=18)
        barChart.set_xticks(x)
        barChart.set_xticklabels(data_stat[0], rotation='vertical', fontsize=10)
        #subplot1.set_yticks(fontsize=10)
        #barChart.legend()
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
        
class StatPage2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='#f2f1f6')

        image_bg = tk.Canvas(self, width=356, height=491)
        self.image_bg_link = tk.PhotoImage(file="assets/folder/bg1.png")
        image_bg.create_image(0, 0, anchor=NW, image=self.image_bg_link)
        image_bg.place(x=192, y= 332, anchor='center')

        image_logo = tk.Canvas(self, width=43, height=30)
        self.image_logo_link = tk.PhotoImage(file="assets/folder/folder.png")
        image_logo.create_image(2, 2, anchor=NW, image=self.image_logo_link)
        image_logo.place(x=49, y= 49, anchor='center')

        self.label_todo = tk.Label(self, text="Category", bg = "#f2f1f6", font=("Calibri 22 bold"))
        self.label_todo.place(x=70, y= 73, anchor='sw')



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()