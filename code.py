
import sqlite3
from hashlib import sha256

master_password = "master_password1000"

password = input("Enter your password:\n")
while password != master_password:
    password = input("What is your password?\n")
    if password == "exit":
        break

connection = sqlite3.connect('pass_manager.db')

def create_password(pass_key, service, admin_pass):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8') + pass_key.encode('utf-8')).hexdigest()[:15]

def get_hex_key(admin_pass, service):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

def get_password(admin_pass, service):
    secret_key = get_hex_key(admin_pass, service)
    cursor = connection.execute("SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')

    file_string = ""
    for row in cursor:
        file_string = row[0]
    return create_password(file_string, service, admin_pass)

def add_password(service, admin_pass):
    secret_key = get_hex_key(admin_pass, service)

    command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' %('"' + secret_key +'"')        
    connection.execute(command)
    connection.commit()
    return create_password(secret_key, service, admin_pass)

if password == master_password:
    try:
        connection.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
        print("Your safe has been created!\nWhat would you like to store in it today?")
    except:
        print("You have a safe, what would you like to do today?")
    
    
    while True:
        print("\n"+ "*"*15)
        print("Commands:")
        print("exit (exit program)")
        print("get (get password)")
        print("generate (generate & store password)")
        print("*"*15)
        input_ = input(":")

        if input_ == "exit":
            break
        if input_ == "generate":
            service = input("What is the name of the service?\n")
            print("\n" + service.capitalize() + " password generated as:\n" + add_password(service, master_password))
        if input_ == "get":
            service = input("What is the name of the service?\n")
            print("\n" + service.capitalize() + " password:\n"+get_password(master_password, service))