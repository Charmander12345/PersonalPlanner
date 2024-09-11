from Classes import updatermodule
import pywinstyles
from hPyT import *
import customtkinter as ctk
import threading
import subprocess
import sys

root = ctk.CTk()
root.title("Updater")
#ctk.set_appearance_mode(DataHandling.getTheme)
#pywinstyles.apply_style(DataHandling.getWindowStyle)
root.minsize(width=400,height=120)
root.resizable(width=False,height=False)
Title = ctk.CTkLabel(root,text="Connecting to GitHub Server...")
Title.place(relx=0.5,rely=0.2,anchor="center")
progress = ctk.CTkProgressBar(root,mode="indeterminate")
progress.place(relx=.5,rely=.5,anchor="center")
progress.start()

def update():
    updater = updatermodule.Updater(repo_url="Charmander12345/PersonalPlanner")
    Title.configure(text="Beginning download...")
    updater.trigger_update()
    Title.configure(text="Reastarting client...")
    subprocess.Popen([sys.executable, "main.py"], creationflags=subprocess.DETACHED_PROCESS)
    root.quit()

updatethread = threading.Thread(target=update)
updatethread.start()
root.mainloop()