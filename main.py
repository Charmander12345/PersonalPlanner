from Classes import App
import os
import DataHandling
if not os.path.exists("Accounts.json"):
    DataHandling.CreateAccountsJSON()
app = App.MyApp()
app.mainloop()