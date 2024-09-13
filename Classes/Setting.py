from typing import Any, Tuple,Callable
import customtkinter as ctk

class Settings(ctk.CTkFrame):
    def __init__(self, master: Any, settingsname:str,optiontype:int,options:list,font:tuple, callback:Callable[[str,str],None], selected_option:str ="", width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None,**kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.settingname=settingsname
        self.optiontype = optiontype
        self.options = options
        self.font = font
        self.callback = callback
        if self.optiontype == 0: #Optionsmenu Widget
            self.Label = ctk.CTkLabel(self,text=self.settingname,font=self.font)
            self.Label.pack(side="left")
            self.optionsmenu = ctk.CTkOptionMenu(self,values=self.options,command=self.OptionsmenuInteract,bg_color="transparent")
            self.optionsmenu.set(selected_option)
            self.optionsmenu.pack(side="right")
        
    def OptionsmenuInteract(self,value):
        self.callback(self.settingname,value)