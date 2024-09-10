import customtkinter as ctk
import tkinter as tk
import sys
import os
from tkinter import filedialog
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Extras')))
import DataHandling
import Errors
import pymsgbox
import time
from datetime import datetime
from PIL import Image, ImageOps
from hPyT import *
import pywinstyles
from CTkMessagebox import *

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Personal Planner")
        self.minsize(width=700,height=400)
        self.loginscreen = ctk.CTkFrame(self)
        self.main_screen = ctk.CTkFrame(self)
        self.loading_screen = ctk.CTkFrame(self)
        self.Font = "Comic Sans MS"
        self.WindowStyle = DataHandling.getWindowStyle()
        self.windowmode = DataHandling.getWindowMode()
        ctk.set_appearance_mode(DataHandling.getTheme())
        if ctk.get_appearance_mode() == "Dark":
            self.ButtonHoverColor = "#4d4d4d"
        elif ctk.get_appearance_mode() == "Light":
            self.ButtonHoverColor = "#C0C0C0"
        else:
            he = ctk.AppearanceModeTracker()
            if he.detect_appearance_mode() == 0:
                self.ButtonHoverColor = "#C0C0C0"
                print("System ist Light Mode")
            else:
                self.ButtonHoverColor = "#4d4d4d"
                print("System ist im Dark Mode")
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW",self.SaveWindowState)
        

    def create_widgets(self):
        self.titleLabel = ctk.CTkLabel(self.loginscreen, text="Personal Planner",font=(self.Font,20))
        self.titleLabel.place(rely=0.1,relx=0.5,anchor="center")
        self.LoginInfo = ctk.CTkLabel(self.loginscreen,text="Login or create an Account",font=(self.Font,18))
        self.LoginInfo.place(rely=0.2,relx=0.5,anchor="center")
        self.Username_Entry = ctk.CTkEntry(self.loginscreen,corner_radius=20,placeholder_text="Username",width=220,font=(self.Font,12))
        self.Username_Entry.place(relx=0.5,rely=0.4,anchor="center")
        self.Password_Entry = ctk.CTkEntry(self.loginscreen,corner_radius=20,placeholder_text="Password",show="*",width=220,font=(self.Font,12))
        self.Password_Entry.place(relx=0.5,rely=0.5,anchor="center")
        self.Login_Button = ctk.CTkButton(self.loginscreen,text="Login",font=(self.Font,16),cursor="hand2",corner_radius=20,command=self.Login)
        self.Login_Button.place(relx=0.5,rely=0.6,anchor="center")
        self.Register_Button = ctk.CTkButton(self.loginscreen,text="Register",font=(self.Font,16),cursor="hand2",corner_radius=20,command=self.Register)
        self.Register_Button.place(relx=0.5,rely=0.7,anchor="center")
        self.loadingbar = ctk.CTkProgressBar(self.loading_screen,mode="indeterminate",width=400)
        self.loadingbar.place(relx=0.5,rely=0.5,anchor="center")
        self.HomeScreen = ctk.CTkFrame(self.main_screen,corner_radius=20)
        self.HomeScreen.place(relx=0.55,rely=0.5,anchor="center",relwidth=0.9,relheight=1)
        self.ClockFrame = ctk.CTkFrame(self.HomeScreen,corner_radius=20)
        self.ClockFrame.bind("<Configure>", self.update_font_size)
        self.ClockLabel = ctk.CTkLabel(self.ClockFrame,text="Clock Display",font=(self.Font,26))
        self.ClockLabel.place(relx=0.5,rely=0.4,anchor="center",relwidth=0.9,relheight=0.9)
        self.DateLabel = ctk.CTkLabel(self.ClockFrame, text="Date Display")
        self.DateLabel.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.9, relheight=0.3)
        self.ClockFrame.place(relx=0.93,rely=0.07,anchor="center",relwidth=0.15,relheight=0.15)
        self.LeftSideBar = ctk.CTkFrame(self.main_screen,corner_radius=0)
        self.LeftSideBar.place(relx=0,rely=0.5,anchor="center",relwidth=0.1,relheight=1)
        self.settingsIcon = ctk.CTkImage(light_image=Image.open("icons\\Settings.png"),dark_image=ImageOps.invert(Image.open("icons\\Settings.png").convert("RGB")))
        self.SettingsButton = ctk.CTkButton(self.LeftSideBar,image=self.settingsIcon,text="",fg_color="transparent",width=30,height=40,corner_radius=40,hover_color=self.ButtonHoverColor,cursor="hand2",command=self.show_settings)
        self.SettingsButton.place(relx=0.75,rely=0.95,anchor="center")
        self.HomeScreenIcon = ctk.CTkImage(light_image=Image.open("icons\\home.png"),dark_image=ImageOps.invert(Image.open("icons\\home.png").convert("RGB")))
        self.HomeButton = ctk.CTkButton(self.LeftSideBar,image=self.HomeScreenIcon,text="",fg_color="transparent",width=30,height=40,corner_radius=40,hover_color=self.ButtonHoverColor,cursor="hand2",command=self.show_settings)
        self.SettingsFrame = ctk.CTkFrame(self.main_screen,corner_radius=20)

        self.show_Login()

    def show_Login(self):
        self.main_screen.pack_forget()
        self.loading_screen.pack_forget()
        self.loginscreen.pack(fill="both",expand=True)
        self.resizable(width=False,height=False)
        self.state("normal")
        self.Username_Entry.configure(state="normal")
        self.Password_Entry.configure(state="normal")
        pywinstyles.apply_style(self,self.WindowStyle)
        self.focus_set()
    
    def show_Main(self):
        self.loginscreen.pack_forget()
        self.loading_screen.pack_forget()
        self.main_screen.pack(fill="both",expand=True)
        self.resizable(width=True,height=True)
        #self.state("zoomed")
        pywinstyles.apply_style(self,self.WindowStyle)
        self.after(1,self.update_time)
        self.after(1,self.update_date)

    def show_Loading(self):
        self.main_screen.pack_forget()
        self.loginscreen.pack_forget()
        self.loading_screen.pack(fill="both",expand=True)
        self.loadingbar.start()
        pywinstyles.apply_style(self,self.WindowStyle)
    
    def show_settings(self):
        self.HomeScreen.place_forget()
        self.SettingsFrame.place(relx=0.55,rely=0.5,anchor="center",relwidth=0.9,relheight=1)
        pywinstyles.apply_style(self,self.WindowStyle)

    def show_home(self):
        self.SettingsFrame.place_forget()
        self.HomeScreen.place(relx=0.55,rely=0.5,anchor="center",relwidth=0.9,relheight=1)
        pywinstyles.apply_style(self,self.WindowStyle)

    def set_active_button(self,button:ctk.CTkButton):
        button.configure(fg_color=self.ButtonHoverColor,hover_color="transparent")

    def SaveWindowState(self):
        DataHandling.writeINI("window","windowmode",self.state())
        DataHandling.writeINI("window","width",str(self.winfo_width()))
        DataHandling.writeINI("window","height",str(self.winfo_height()))
        DataHandling.writeINI("customization","theme",ctk.get_appearance_mode())
        DataHandling.writeINI("customization","style",self.WindowStyle)
        self.destroy()

    def Login(self):
        Username = self.Username_Entry.get()
        Password = self.Password_Entry.get()
        self.Username_Entry.delete(0,ctk.END)
        self.Password_Entry.delete(0,ctk.END)
        self.Username_Entry.configure(state="disabled")
        self.Password_Entry.configure(state="disabled")
        self.focus_set()
        try:
            if DataHandling.LOGIN(Username=Username,Password=Password):
                self.LoadAccountData(Username)
        except Errors.UnknownAccountError as e:
            CTkMessagebox(self,title="UnknownAccountError",message=e,icon="cancel",cancel_button="None")
            #pymsgbox.alert(e,"UnknownAccountError")
            self.Username_Entry.configure(state="normal")
            self.Password_Entry.configure(state="normal")
        except Errors.PasswordIncorrectError as e:
            CTkMessagebox(self,title="IncorrectPasswordError",message=e,icon="cancel")
            #pymsgbox.alert(e,"PasswordIncorrectError")
            self.Username_Entry.configure(state="normal")
            self.Password_Entry.configure(state="normal")
        except Errors.AccountsFileNotFoundError as e:
            CTkMessagebox(self,title="AccountsFileNotFoundError",message=e,icon="warning")
            #pymsgbox.alert(e,"AccountsFileNotFoundError")
            self.Username_Entry.configure(state="normal")
            self.Password_Entry.configure(state="normal")
    
    def Register(self):
        Username = self.Username_Entry.get()
        Password = self.Password_Entry.get()
        self.Username_Entry.delete(0,ctk.END)
        self.Password_Entry.delete(0,ctk.END)
        self.Username_Entry.configure(state="disabled")
        self.Password_Entry.configure(state="disabled")
        self.focus_set()
        try:
            if DataHandling.REGISTER(Username,Password):
                self.Username_Entry.configure(state="normal")
                self.Password_Entry.configure(state="normal")

        except Errors.AccountAlreadyExistsError as e:
            CTkMessagebox(self,title="AccountAlreadyExistsError",message=e,icon="cancel")
            #pymsgbox.alert(e,"AccountAlreadyExistsError")
            self.Username_Entry.configure(state="normal")
            self.Password_Entry.configure(state="normal")

    def LoadAccountData(self,Username):
        try:
            self.show_Loading()
            DataHandling.LOADACCOUNTDATA(Username)
            self.show_Main()
        except Errors.AccountDataNotFoundError as e:
            CTkMessagebox(self,title="AccountDataNotFoundError",message=e,icon= "warning")
            #pymsgbox.alert(e,"AccountDataNotFoundError")
            self.Username_Entry.configure(state="normal")
            self.Password_Entry.configure(state="normal")
            self.show_Login()

    def update_time(self):
    # Uhrzeit im Format "Stunden:Minuten" erhalten
        current_time = time.strftime("%H:%M")
        self.ClockLabel.configure(text=current_time)

    # Berechnung, wann die nächste volle Minute ist
        current_seconds = int(time.strftime("%S"))
        remaining_time = (60 - current_seconds) * 1000  # Millisekunden bis zur nächsten vollen Minute

    # Timer für das nächste Update auf die volle Minute setzen
        self.after(remaining_time, self.update_time)

    def update_date(self):
        current_date = datetime.now().strftime("%d.%m.%Y")
        self.DateLabel.configure(text=current_date)
        now = datetime.now()
        seconds_until_midnight = ((24 - now.hour - 1) * 3600) + ((60 - now.minute - 1) * 60) + (60 - now.second)
        self.after(seconds_until_midnight * 1000, self.update_date)

    def update_font_size(self,event):
        # Breite und Höhe des Frames abfragen
        frame_width = self.ClockFrame.winfo_width()
        frame_height = self.ClockFrame.winfo_height()

        # Schriftgröße proportional zur Größe des Frames setzen (z.B. basierend auf der Höhe)
        new_font_size = min(frame_width, frame_height) // 4  # Hier kannst du die Skalierung anpassen
        new_font_size_date = min(frame_width, frame_height) // 6

        # Schriftgröße im Label aktualisieren
        self.ClockLabel.configure(font=(self.Font, new_font_size))
        self.DateLabel.configure(font=(self.Font, new_font_size_date))