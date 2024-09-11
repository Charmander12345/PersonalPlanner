from typing import Any, Tuple
import customtkinter as ctk

class Settings(ctk.CTkFrame):
    def __init__(self, master: Any, settingsname:str,optiontype:int,options:list,font:tuple, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None,**kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.settingname=settingsname
        self.optiontype = optiontype
        self.options = options
        self.font = font
        if self.optiontype == 0: #Optionsmenu Widget
            self.Label = ctk.CTkLabel(self,text=self.settingname,font=self.font)
            self.Label.place(relx=0.5,rely=0.3,anchor="center")
            self.optionsmenu = ctk.CTkOptionMenu(self,values=self.options)
            self.optionsmenu.place(relx=0.5,rely=0.6,anchor="center")