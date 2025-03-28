import psutil
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
import smtplib
from email.mime.text import MIMEText
from plyer import notification
import pyttsx3  # For voice alerts
import time  # For flashing effect
import threading  # To avoid GUI freezing

# =================== CONFIGURATIONS ===================
blacklist = ["malware.exe", "virus.exe", "keylogger.exe"]  # Add more threats here
whitelist = ["explorer.exe", "notepad.exe", "cmd.exe"]  # Trusted processes

# Email Alert Settings (Replace with your email)
EMAIL_FROM = "abhisaroj226002@gmail.com"
EMAIL_TO = "chutki144401@gmail.com"
EMAIL_PASSWORD = "tflzjtguabrhtyyp"

scanning = False  # To control scanning state

# =================== EMAIL ALERT FUNCTION ===================
def send_email_alert(process_name):
    msg = MIMEText(f"⚠ Alert: {process_name} was detected and terminated!")
    msg["Subject"] = "🚨 Threat Detected!"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
            log_message(f"📧 Email alert sent for {process_name}")
    except Exception as e:
        log_message(f"⚠ Failed to send email: {e}")

# =================== FLASHING SCREEN FUNCTION ===================
def flash_screen():
    for _ in range(5):  # Flash 5 times
        root.configure(bg="red")
        time.sleep(0.5)
        root.configure(bg="#222831")
        time.sleep(0.5)

# =================== VOICE ALERT FUNCTION ===================
def voice_alert(process_name):
    engine = pyttsx3.init()
    engine.say(f"Warning! {process_name} detected and terminated.")
    engine.runAndWait()

# =================== THREAT DETECTION FUNCTION ===================
def scan_and_terminate():
    if not scanning:
        return

    for process in psutil.process_iter(attrs=["pid", "name"]):
        try:
            process_name = process.info["name"]
            process_pid = process.info["pid"]

            if process_name.lower() in blacklist:
                os.system(f"taskkill /F /PID {process_pid}")
                log_message(f"🔴 Threat Terminated: {process_name} (PID: {process_pid})")

                # Show System Notification
                notification.notify(
                    title="🚨 Threat Detected!",
                    message=f"{process_name} has been terminated!",
                    timeout=5
                )

                # Start alert mechanisms
                threading.Thread(target=flash_screen).start()
                threading.Thread(target=voice_alert, args=(process_name,)).start()
                threading.Thread(target=send_email_alert, args=(process_name,)).start()

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    root.after(5000, scan_and_terminate)  # Run every 5 seconds

# =================== GUI FUNCTIONS ===================
def start_scanning():
    global scanning
    scanning = True
    log_message("🔍 Scanning started...")
    scan_and_terminate()

def stop_scanning():
    global scanning
    scanning = False
    log_message("⏸ Scanning stopped.")

def clear_logs():
    text_area.delete(1.0, tk.END)

def log_message(message):
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
    text_area.insert(tk.END, message + "\n")
    text_area.see(tk.END)

# =================== GUI SETUP ===================
root = tk.Tk()
root.title("🚀 Dynamic Threat Response System")
root.geometry("600x400")
root.configure(bg="#222831")

# Title Label
title_label = tk.Label(root, text="Dynamic Threat Response System", font=("Arial", 14, "bold"), fg="white", bg="#222831")
title_label.pack(pady=10)

# Scrolling Text Area (Threat Logs)
text_area = scrolledtext.ScrolledText(root, width=70, height=12, bg="#393E46", fg="white", font=("Consolas", 10))
text_area.pack()

# Control Buttons
btn_frame = tk.Frame(root, bg="#222831")
btn_frame.pack(pady=10)

start_btn = tk.Button(btn_frame, text="▶ Start", command=start_scanning, width=12, bg="#00ADB5", fg="white", font=("Arial", 10, "bold"))
start_btn.grid(row=0, column=0, padx=5)

stop_btn = tk.Button(btn_frame, text="⏹ Stop", command=stop_scanning, width=12, bg="#FF5722", fg="white", font=("Arial", 10, "bold"))
stop_btn.grid(row=0, column=1, padx=5)

clear_btn = tk.Button(btn_frame, text="🧹 Clear Logs", command=clear_logs, width=12, bg="#607D8B", fg="white", font=("Arial", 10, "bold"))
clear_btn.grid(row=0, column=2, padx=5)

# Run the GUI
root.mainloop()
