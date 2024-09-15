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
from Classes import Setting,updatermodule
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ADDONS')))
from Extras import ctk_components
import threading
import subprocess
import pathlib
from CTkToolTip import *
from notifypy import Notify


class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Personal Planner")
        self.minsize(width=700,height=400)
        self.Font = "Comic Sans MS"
        self.WindowStyle = DataHandling.getWindowStyle()
        self.windowmode = DataHandling.getWindowMode()
        self.updater = updatermodule.Updater("Charmander12345/PersonalPlanner","Classes/__init__.py")
        ctk.set_appearance_mode(DataHandling.getAPMode())
        self.APMode = DataHandling.getAPMode()
        ctk.set_default_color_theme(DataHandling.getTheme())
        self.theme = DataHandling.getTheme()
        self.protocol("WM_DELETE_WINDOW",self.SaveWindowState)
        self.logged_in = False
        self.create_widgets()
        
    def create_widgets(self):
        self.loginscreen = ctk.CTkFrame(self)
        self.main_screen = ctk.CTkFrame(self)
        self.loading_screen = ctk.CTkFrame(self)
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
        if getattr(sys, 'frozen', False):
            self.base_path = pathlib.Path(sys._MEIPASS)
        else:
            self.base_path = pathlib.Path(".")
        self.settingsIcon = ctk.CTkImage(light_image=Image.open(self.base_path / "icons/Settings_light.png"),dark_image=Image.open(self.base_path / "icons/Settings_dark.png"))
        self.SettingsButton = ctk.CTkButton(self.LeftSideBar,image=self.settingsIcon,text="",fg_color="transparent",width=30,height=40,corner_radius=40,cursor="hand2",command=self.show_settings)
        self.SettingsToolTip = CTkToolTip(widget=self.SettingsButton,message="Go to settings page",delay=1)
        self.SettingsButton.place(relx=0.75,rely=0.95,anchor="center")
        #Home
        self.HomeScreenIcon = ctk.CTkImage(light_image=Image.open(self.base_path / "icons/home_light.png"),dark_image=Image.open(self.base_path / "icons/home_dark.png"))
        self.HomeButton = ctk.CTkButton(self.LeftSideBar,image=self.HomeScreenIcon,text="",fg_color="transparent",width=30,height=40,corner_radius=40,cursor="hand2",command=self.show_home)
        self.HomeToolTip = CTkToolTip(message="Go to the home page",widget=self.HomeButton,delay=1)
        self.HomeButton.place(relx=0.75,rely=0.05,anchor="center")
        #Mail
        self.MailFrame = ctk.CTkFrame(self.main_screen,corner_radius=20)
        self.MailIcon = ctk.CTkImage(light_image=Image.open(self.base_path/"icons/mail_light.png"),dark_image=Image.open(self.base_path/"icons/mail_dark.png"))
        self.MailButton = ctk.CTkButton(self.LeftSideBar,image=self.MailIcon,text="",fg_color="transparent",width=30,height=40,corner_radius=40,cursor="hand2",command=self.show_mail)
        self.MailToolTip = CTkToolTip(widget=self.MailButton,message="Go to the mail page",delay=1)
        self.MailButton.place(relx=0.75,rely=0.15,anchor="center")
        self.MailTitleFrame = ctk.CTkFrame(self.MailFrame,corner_radius=20,height=40,width=200)
        self.MailTitleFrame.place(rely=0.05,relx=0.5,anchor="center")
        self.MailLabel = ctk.CTkLabel(self.MailTitleFrame,text="Mail",font=(self.Font,20))
        self.MailLabel.place(relx=0.5,rely=0.5,anchor="center")
        #Mail Login
        self.MailLoginFrame = ctk.CTkFrame(self.MailFrame,corner_radius=20)
        self.MailUsername = ctk.CTkEntry(self.MailLoginFrame,corner_radius=20,placeholder_text="Username")
        self.MailPassword = ctk.CTkEntry(self.MailLoginFrame,corner_radius=20,placeholder_text="Password",show="*")
        self.MailLoginLabel = ctk.CTkLabel(self.MailLoginFrame,text="Login to your email account",font=(self.Font,20))
        self.MailLoginButton = ctk.CTkButton(self.MailLoginFrame,text="Login",font=(self.Font,16),cursor="hand2",corner_radius=20)
        self.MailLoginButton.place(relx=0.5,rely=0.65,anchor="center")
        self.MailPassword.place(relx=0.5,rely=0.5,anchor="center",relwidth=0.4)
        self.MailUsername.place(relx=0.5,rely=0.35,anchor="center",relwidth=0.4)
        self.MailLoginLabel.place(relx=0.5,rely=0.1,anchor="center")
        self.MailLoginFrame.place(relx=0.5,rely=0.5,anchor="center",relwidth=0.6,relheight=0.6)
        #Calender
        self.CalenderFrame = ctk.CTkFrame(self.main_screen,corner_radius=20)
        self.CalenderIcon = ctk.CTkImage(light_image=Image.open(self.base_path/"icons/calender_light.png"),dark_image=Image.open(self.base_path/"icons/calender_dark.png"))
        self.CalenderButton = ctk.CTkButton(self.LeftSideBar,image=self.CalenderIcon,text="",fg_color="transparent",width=30,height=40,corner_radius=40,cursor="hand2",command=self.show_calender)
        self.CalenderToolTip = CTkToolTip(widget=self.CalenderButton,message="Go to the calender page",delay=1)
        self.CalenderButton.place(relx=0.75,rely=0.25,anchor="center")
        self.CalenderTitleFrame = ctk.CTkFrame(self.CalenderFrame,corner_radius=20,height=40,width=200)
        self.CalenderTitleFrame.place(rely=0.05,relx=0.5,anchor="center")
        self.CalenderLabel = ctk.CTkLabel(self.CalenderTitleFrame,text="Calender",font=(self.Font,20))
        self.CalenderLabel.place(relx=0.5,rely=0.5,anchor="center")
        #Settings
        self.SettingsFrame = ctk.CTkFrame(self.main_screen,corner_radius=20)
        self.AppearanceMode = Setting.Settings(master=self.SettingsFrame,settingsname="Appearance Mode",optiontype=0,options=["Light","Dark"],font=(self.Font,16),callback=self.handle_option_selection,selected_option=self.APMode)
        self.AppearanceMode.pack(fill="x", expand=True,padx=2)
        self.ColorTheme = Setting.Settings(self.SettingsFrame,"Color Theme",0,["blue","dark blue","green","Lauren"],font=(self.Font,16),callback=self.handle_option_selection,selected_option=self.theme)
        self.ColorTheme.pack(fill="x",expand=True,padx=2)
        #Display the loginscreen
        if not self.logged_in:
            self.show_Login()
            #Check for updates in the background
            self.updatethread = threading.Thread(target=self.check_for_update)
            self.updatethread.start()
        else:
            self.show_Main()
        

    def show_Login(self):
        window_frame.center(self)
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
        self.MailFrame.place_forget()
        self.CalenderFrame.place_forget()
        self.SettingsFrame.place(relx=0.55,rely=0.5,anchor="center",relwidth=0.9,relheight=1)
        pywinstyles.apply_style(self,self.WindowStyle)

    def show_home(self):
        self.SettingsFrame.place_forget()
        self.MailFrame.place_forget()
        self.CalenderFrame.place_forget()
        self.HomeScreen.place(relx=0.55,rely=0.5,anchor="center",relwidth=0.9,relheight=1)
        pywinstyles.apply_style(self,self.WindowStyle)

    def show_mail(self):
        self.SettingsFrame.place_forget()
        self.HomeScreen.place_forget()
        self.CalenderFrame.place_forget()
        self.MailFrame.place(relx=0.55,rely=0.5,anchor="center",relwidth=0.9,relheight=1)
        pywinstyles.apply_style(self,self.WindowStyle)

    def show_calender(self):
        self.SettingsFrame.place_forget()
        self.HomeScreen.place_forget()
        self.MailFrame.place_forget()
        self.CalenderFrame.place(relx=0.55,rely=0.5,anchor="center",relwidth=0.9,relheight=1)
        pywinstyles.apply_style(self,self.WindowStyle)

    def set_active_button(self,button:ctk.CTkButton):
        button.configure(fg_color=self.ButtonHoverColor,hover_color="transparent")

    def SaveWindowState(self):
        DataHandling.writeINI("window","windowmode",self.state())
        DataHandling.writeINI("window","x",str(self.winfo_width()))
        DataHandling.writeINI("window","y",str(self.winfo_height()))
        DataHandling.writeINI("customization","mode",self.APMode)
        DataHandling.writeINI("customization","theme",self.theme)
        DataHandling.writeINI("customization","style",self.WindowStyle)
        self.destroy()

    def Login(self):
        Username = self.Username_Entry.get()
        Password = self.Password_Entry.get()
        self.Username_Entry.configure(state="disabled")
        self.Password_Entry.configure(state="disabled")
        self.focus_set()
        try:
            if DataHandling.LOGIN(Username=Username,Password=Password):
                self.LoadAccountData(Username)
                self.logged_in = True
        except Errors.UnknownAccountError as e:
            CTkMessagebox(self,title="UnknownAccountError",message=e,icon="cancel",cancel_button="None")
            #pymsgbox.alert(e,"UnknownAccountError")
            self.Username_Entry.configure(state="normal")
            self.Password_Entry.configure(state="normal")
            self.Username_Entry.delete(0,ctk.END)
            self.Password_Entry.delete(0,ctk.END)
        except Errors.PasswordIncorrectError as e:
            CTkMessagebox(self,title="IncorrectPasswordError",message=e,icon="cancel")
            #pymsgbox.alert(e,"PasswordIncorrectError")
            self.Username_Entry.configure(state="normal")
            self.Password_Entry.configure(state="normal")
            self.Password_Entry.delete(0,ctk.END)
        except Errors.AccountsFileNotFoundError as e:
            CTkMessagebox(self,title="AccountsFileNotFoundError",message=e,icon="warning")
            #pymsgbox.alert(e,"AccountsFileNotFoundError")
            self.Username_Entry.configure(state="normal")
            self.Password_Entry.configure(state="normal")
    
    def Register(self):
        Username = self.Username_Entry.get()
        Password = self.Password_Entry.get()
        self.Username_Entry.configure(state="disabled")
        self.Password_Entry.configure(state="disabled")
        self.focus_set()
        try:
            if DataHandling.REGISTER(Username,Password):
                #self.Username_Entry.configure(state="normal")
                #self.Password_Entry.configure(state="normal")
                self.Login()

        except Errors.AccountAlreadyExistsError as e:
            CTkMessagebox(self,title="AccountAlreadyExistsError",message=e,icon="cancel")
            #pymsgbox.alert(e,"AccountAlreadyExistsError")
            self.Username_Entry.configure(state="normal")
            self.Password_Entry.configure(state="normal")
            self.Username_Entry.delete(0,ctk.END)
            self.Password_Entry.delete(0,ctk.END)

        except Errors.AccountsFileNotFoundError as e:
            CTkMessagebox(self,title="AccountsFileNotFoundError",message=e,icon="warning")
            #pymsgbox.alert(e,"AccountsFileNotFoundError")
            self.Username_Entry.configure(state="normal")
            self.Password_Entry.configure(state="normal")

    def LoadAccountData(self,Username):
        try:
            self.show_Loading()
            DataHandling.LOADACCOUNTDATA(Username)
            self.show_Main()
            x,y = DataHandling.getWindowXY()
            self.state(DataHandling.getWindowMode())
            #window_frame.resize(self,width=x,height=y)
            #window_frame.center(self)
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
        mail_frame_height = self.MailFrame.winfo_height()
        mail_frame_width = self.MailFrame.winfo_width()

        # Schriftgröße proportional zur Größe des Frames setzen (z.B. basierend auf der Höhe)
        new_font_size = min(frame_width, frame_height) // 4  # Hier kannst du die Skalierung anpassen
        new_font_size_date = min(frame_width, frame_height) // 6
        new_font_size_Mail = min(mail_frame_width, mail_frame_height) // 2
        # Schriftgröße im Label aktualisieren
        self.ClockLabel.configure(font=(self.Font, new_font_size))
        self.DateLabel.configure(font=(self.Font, new_font_size_date))
        self.MailLoginLabel.configure(font=(self.Font, new_font_size_Mail))

    def handle_option_selection(self,settingsname:str,value:str):
        if settingsname == "Appearance Mode":
            if value == "Dark":
                ctk.set_appearance_mode(value)
                self.APMode = "Dark"
            elif value == "Light":
                ctk.set_appearance_mode(value)
                self.APMode = "Light"
        elif settingsname == "Color Theme":
            if value == "blue":
                ctk.set_default_color_theme("blue")
                self.update()
                self.theme = "blue"
            elif value == "dark blue":
                ctk.set_default_color_theme("dark-blue")
                self.update()
                self.theme = "dark-blue"
            elif value == "green":
                ctk.set_default_color_theme("green")
                self.update()
                self.theme = "green"
            elif value == "Lauren":
                ctk.set_default_color_theme("Lauren")
                self.update()
                self.theme = "Lauren"
            restartbanner = ctk_components.CTkBanner(self,state="info",title="Restart to apply changes?",btn1="Restart now",btn2="Not now")
            if restartbanner.get() == "Restart now":
                self.reload_widgets()

    def check_for_update(self):
        if self.updater.check_for_update():
            self.updatebanner = ctk_components.CTkBanner(self,state="info",title="Update available",btn1="Install now",btn2="Cancel")
            if self.updatebanner.get() == "Install now":
                self.progress = ctk_components.CTkProgressPopup(self,title="Updating now",message="Fetching update from GitHub...")
                print("installation confirmed")
                subprocess.Popen([sys.executable, "Updater.py"], creationflags=subprocess.DETACHED_PROCESS)
                print("starting subprocess")
                self.quit()
                quit()
        elif self.updater.check_for_update() == None:
            self.updatebanner = ctk_components.CTkNotification(self,state="error",message="Version data damaged. Updates may not work as intended")
            time.sleep(4)
            try:
                self.updatebanner.destroy()
            except RuntimeError:
                pass
        else:
            self.updatebanner = ctk_components.CTkNotification(self,state="info",message="Client Version up to date")
            time.sleep(4)
            try:
                self.updatebanner.destroy()
            except RuntimeError:
                pass

    def reload_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()