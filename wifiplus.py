import subprocess
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def get_saved_wifi_networks():
    command = 'netsh wlan show profiles'
    result = subprocess.run(command, capture_output=True, text=True, encoding='cp850')
    
    if result.returncode == 0:
        output = result.stdout
        pattern_name = r':\s*(.*)'
        pattern_password_en = r'Key Content\s*: (.*)'
        pattern_password_de = r'Schlüsselinhalt\s*: (.*)'
        
        profiles = re.findall(pattern_name, output)
        wifi_networks = {}
        
        for profile in profiles:
            command = f'netsh wlan show profile name="{profile}" key=clear'
            result = subprocess.run(command, capture_output=True, text=True, encoding='cp850')
            
            if result.returncode == 0:
                profile_output = result.stdout
                
                password_match_en = re.search(pattern_password_en, profile_output)
                password_match_de = re.search(pattern_password_de, profile_output)
                
                if password_match_en:
                    password = password_match_en.group(1)
                elif password_match_de:
                    password = password_match_de.group(1)
                else:
                    password = None
                    
                wifi_networks[profile] = password
            else:
                wifi_networks[profile] = None
        
        return wifi_networks
    else:
        messagebox.showerror("Error", "Error occurred while retrieving Wi-Fi profiles.")
        return {}

def save_as_text_file():
    wifi_networks = get_saved_wifi_networks()
    
    if wifi_networks:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    for wifi, password in wifi_networks.items():
                        if password:
                            file.write(f"Wi-Fi Name: {wifi} - Password: {password}\n")
                        else:
                            file.write(f"Wi-Fi Name: {wifi} - Password: Not available\n")
                    file.write(f'\nMade with Wi-Fi Networks (Python - Made by iLollek - https://github.com/iLollek/Wifi-Network-Password-Info)')
                messagebox.showinfo("File Saved", "Wi-Fi information saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file:\n{str(e)}")
        else:
            messagebox.showwarning("File Not Saved", "No file path selected.")
    else:
        messagebox.showwarning("No Wi-Fi Networks", "No saved Wi-Fi networks found.")

# Create Tkinter window
window = tk.Tk()
window.title("Wi-Fi Networks")
window.geometry("400x300")

# Create Listbox
listbox = tk.Listbox(window, width=50)
listbox.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

# Create Save button
save_button = tk.Button(window, text="Save as .txt", command=save_as_text_file)
save_button.pack(pady=5)

# Get Wi-Fi networks
wifi_networks = get_saved_wifi_networks()

# Populate Listbox with Wi-Fi names and passwords
for wifi, password in wifi_networks.items():
    if password:
        listbox.insert(tk.END, f"Wi-Fi Name: {wifi} - Password: {password}\n")
    else:
        listbox.insert(tk.END, f"Wi-Fi Name: {wifi} - Password: Not available\n")

# Run the Tkinter event loop
window.mainloop()
