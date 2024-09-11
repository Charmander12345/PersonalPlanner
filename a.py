import customtkinter as ctk
from PIL import Image,ImageOps

root = ctk.CTk()
ctk.set_appearance_mode("Light")
HomeScreenIcon = ctk.CTkImage(light_image=Image.open("icons\\home.png"),dark_image=ImageOps.invert(Image.open("icons\\home.png").convert("RGB")))
HomeButton = ctk.CTkButton(root,image=HomeScreenIcon,text="",fg_color="transparent",width=30,height=40,corner_radius=40,hover_color="#333333",cursor="hand2")
HomeButton.place(relx=.5,rely=0.5,anchor="center")
root.mainloop()