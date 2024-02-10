
from cryptography.fernet import Fernet
import json
import os
import tkinter as tk
from tkinter import messagebox
import hashlib

class PasswordManager:
    def __init__(self):
        self.key = None
        self.file = 'passwords.json'
        self.passwords = {}
        self.master_password = None

    def authenticate(self, entered_password):
        hashed_password = hashlib.sha256(entered_password.encode()).hexdigest()
        return hashed_password == self.master_password

    def load_key(self):
        key_file = 'key.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as file:
                self.key = file.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_file, 'wb') as file:
                file.write(self.key)

    def load_passwords(self):
        try:
            with open(self.file, 'rb') as file:
                data = file.read()
                if data:
                    decrypted_data = Fernet(self.key).decrypt(data)
                    self.passwords = json.loads(decrypted_data)
        except FileNotFoundError:
            pass

    def save_passwords(self):
        with open(self.file, 'wb') as file:
            encrypted_data = Fernet(self.key).encrypt(json.dumps(self.passwords).encode())
            file.write(encrypted_data)

    def add_password(self, service, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.passwords[service] = {'username': username, 'password': hashed_password}
        self.save_passwords()
        messagebox.showinfo("Success", f"Password for '{service}' added successfully.")

    def get_password(self, service):
        if service in self.passwords:
            return self.passwords[service]
        else:
            messagebox.showerror("Error", f"Password for '{service}' not found.")

    def list_services(self):
        service_list = "\nStored Services:\n"
        for service in self.passwords:
            service_list += service + "\n"
        messagebox.showinfo("Stored Services", service_list)

    def display_passwords(self):
        password_list = "\nStored Passwords:\n"
        for service, info in self.passwords.items():
            password_list += f"Service: {service}\nUsername: {info['username']}\nPassword: {info['password']}\n\n"
        messagebox.showinfo("Stored Passwords", password_list)

def set_master_password():
    global manager
    master_password = master_password_entry.get()
    if master_password:
        hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
        manager.master_password = hashed_password
        manager.load_key()
        manager.load_passwords()
        messagebox.showinfo("Success", "Master Password Set Successfully.")
        root.destroy()
    else:
        messagebox.showerror("Error", "Please enter a valid master password.")

def add_password():
    service = service_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if service and username and password:
        manager.add_password(service, username, password)
        service_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def retrieve_password():
    service = service_entry.get()
    password_info = manager.get_password(service)
    if password_info:
        messagebox.showinfo("Password Info", f"Username: {password_info['username']}\nPassword: {password_info['password']}")
    else:
        messagebox.showerror("Error", f"Password for '{service}' not found.")

def list_services():
    manager.list_services()

def display_passwords():
    manager.display_passwords()

def exit_app():
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Set Master Password")

master_password_label = tk.Label(root, text="Enter Master Password: ")
master_password_label.pack()

master_password_entry = tk.Entry(root, show='*')
master_password_entry.pack()

set_password_button = tk.Button(root, text="Set Password", command=set_master_password)
set_password_button.pack()

manager = PasswordManager()  # Create manager instance before main loop

root.mainloop()

# Validation for master password set
if not manager.master_password:
    messagebox.showerror("Authentication Failed", "Master password not set. Exiting.")
    exit()

# GUI for password manager
root = tk.Tk()
root.title("Password Manager")

# Labels and Entries
tk.Label(root, text="Service: ").grid(row=0, column=0)
tk.Label(root, text="Username: ").grid(row=1, column=0)
tk.Label(root, text="Password: ").grid(row=2, column=0)

service_entry = tk.Entry(root)
username_entry = tk.Entry(root)
password_entry = tk.Entry(root, show='*')

service_entry.grid(row=0, column=1)
username_entry.grid(row=1, column=1)
password_entry.grid(row=2, column=1)

# Buttons
add_button = tk.Button(root, text="Add Password", command=add_password)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

retrieve_button = tk.Button(root, text="Retrieve Password", command=retrieve_password)
retrieve_button.grid(row=4, column=0, columnspan=2, pady=10)

list_button = tk.Button(root, text="List Services", command=list_services)
list_button.grid(row=5, column=0, columnspan=2, pady=10)

display_button = tk.Button(root, text="All Accounts", command=display_passwords)
display_button.grid(row=6, column=0, columnspan=2, pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()
