import os
import configparser
from werkzeug.security import generate_password_hash,check_password_hash
import Errors
import json
import pathlib

config = configparser.ConfigParser()
config.read("client.ini")
accountfile = pathlib.Path("Accounts.json")

def writeINI(Section:str, Key:str, value:str):
    global config
    if Section not in config:
        config.add_section(Section)
    config[Section][Key] = value
    
    # Schreibe die Änderungen zurück in die .ini Datei
    with open(f"client.ini", "w") as configfile:
        config.write(configfile)

def getWindowMode():
    try:
        return config["window"]["windowmode"]
    except KeyError:
        writeINI("window","windowmode","normal")
        return "normal"

def getTheme():
    try:
        return config["customization"]["theme"]
    except KeyError:
        writeINI("customization","theme","System")
        return "System"
    
def getWindowStyle():
    try:
        return config["customization"]["style"]
    except KeyError:
        writeINI("customization","style","optimised")
        return "optimised"
    
def getWindowXY():
    try:
        x = int(config["window"]["x"])
        y = int(config["window"]["y"])
        return x,y
    except KeyError:
        writeINI("window","x","700")
        writeINI("window","y","400")
        return 700,400
def getLoginState():
    try:
        if config["data"]["loginstate"] == "true":
            return True
        else:
            return False
    except KeyError:
        writeINI("data","loginstate","false")
        return False
    
def LOGIN(Username,Password):
    accountfile = pathlib.Path("Accounts.json")
    if accountfile.exists():
        with open("Accounts.json", 'r') as file:
            data = json.load(file)
    else:
        CreateAccountsJSON()
        raise Errors.AccountsFileNotFoundError
        

    for account in data["accounts"]:
        if account["username"] == Username:
            if check_password_hash(account["password_hash"],Password):
                return True
            else:
                raise Errors.PasswordIncorrectError
    raise Errors.UnknownAccountError

def CreateAccountsJSON():
    """Erstelle eine JSON-Datei mit der Kategorie 'accounts'."""
    initial_data = {
        "accounts": []
    }
    
    # Die Datei erstellen und die Anfangsdaten schreiben
    with open("Accounts.json", 'w') as file:
        json.dump(initial_data, file, indent=4)

def REGISTER(Username,Password):
    Password_HASH = generate_password_hash(Password)
    """Erstelle ein neues Konto und speichere es in der JSON-Datei."""
    if accountfile.exists():
        # JSON-Datei laden
        with open("Accounts.json", 'r') as file:
            data = json.load(file)
    else:
        CreateAccountsJSON()
        raise Errors.AccountsFileNotFoundError
    
    # Prüfen, ob der Benutzername bereits existiert
    for account in data["accounts"]:
        if account["username"] == Username:
            raise Errors.AccountAlreadyExistsError
    os.mkdir(f"{Username}")
    f = open(f"{Username}\\{Username}_profile.data","w")
    config = configparser.ConfigParser()
    config.read(f"{Username}_profile.data")
    config.add_section("customization")
    config["customization"]["theme"] = "Dark"
    config["customization"]["color"] = "#333333"
    config.add_section("data")
    config.write(f)
    f.close()
    # Neues Konto hinzufügen
    new_account = {
        "username": Username,
        "password_hash": Password_HASH,
        "data_path": f"{Username}\\{Username}_profile.data"
    }
    data["accounts"].append(new_account)
    
    # Daten in der JSON-Datei speichern
    with open("Accounts.json", 'w') as file:
        json.dump(data, file, indent=4)
    return True

def LOADACCOUNTDATA(Username):
    global path
    path = ""
    if accountfile.exists():
        with open("Accounts.json", 'r') as file:
            data = json.load(file)
    else:
        raise Errors.AccountsFileNotFoundError
    for account in data["accounts"]:
        if account["username"] == Username:
            path = account["data_path"]
    if pathlib.Path(path).exists():
        accountreader = configparser.ConfigParser()
        accountreader.read(path)
        return accountreader
    else:
        raise Errors.AccountDataNotFoundError

def SAVEACCOUNTDATA(Username):
    config=configparser.ConfigParser()
    config.read(path)
    config["customization"]["theme"] = "dark"
    config["customization"]["color"] = "#333333"
    with open(path, "w") as configfile:
        config.write(configfile)
    