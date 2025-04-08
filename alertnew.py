import tkinter as tk
import time

def flash_screen():
    for _ in range(5):
        root.configure(bg="red")
        time.sleep(0.5)
        root.configure(bg="#222831")
        time.sleep(0.5)

root = tk.Tk()
root.title("🚨 Threat Alert")
root.geometry("300x150")
root.configure(bg="#222831")

label = tk.Label(root, text="⚠ Malware Detected!", font=("Arial", 14, "bold"), fg="white", bg="#222831")
label.pack(pady=20)

flash_screen()
root.mainloop()
