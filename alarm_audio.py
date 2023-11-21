import asyncio
import os
import datetime
from playsound import playsound
import smtplib
from email.mime.text import MIMEText
from secret import email_pass
import webbrowser 
import time
import threading
from plyer import notification

smtp_server = "smtp.gmail.com"
smtp_port = 465
my_email = "rohanfalwariya2@gmail.com"
    # my_email = "rohanfalwariya2@gmail.com"

class NotificationThread(threading.Thread):
    def __init__(self):
        super(NotificationThread, self).__init__()
        self.stop_notification = False

    def run(self):
        try:
            while not self.stop_notification:
                notification.notify(
                    title="Drink water and take a short break 😊",
                    message='''To avoid becoming dehydrated, it's best to drink plenty of fluids — as much as 2-3 cups per hour''',
                    timeout=2
                )
                time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Notification thread stopped.")

class Alarm:
    async def set_alarm(self, alarm_hour: int, alarm_min: int, alarm_am: str):
        while True:
            now = datetime.datetime.now()
            if alarm_hour == now.hour and alarm_min == now.minute:
                audio_file = os.path.dirname(__file__) + "/audio.mp3"
                playsound(audio_file)
                break
            await asyncio.sleep(10)  # Check every 10 seconds




    def set_email(self, alarm_hour: int, alarm_min: int, alarm_am: str, data:str, subject:str,to:str):
        if alarm_am == "pm" and alarm_hour != 12:
            alarm_hour += 12
            
        while True:
            now = datetime.datetime.now()
            if alarm_hour == now.hour and alarm_min == now.minute:     
                msg = MIMEText(data)
                msg['Subject'] = subject
                msg['From'] = my_email
                msg['To'] = to

                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
                server.login(my_email, email_pass)
                server.send_message(msg)
                server.quit()
                break

class EmailNotification:

    # email_pass="fpza fnkc jfmy fdsx"
    # smtp_server = "smtp.gmail.com"
    # smtp_port = 465
    # email_pass = "Rohan2050"  # Replace with your actual email password

    @staticmethod
    def send_email(alarm_hour: int, alarm_min: int, alarm_am: str, data: str, subject: str, to: str):
        if alarm_am == "pm" and alarm_hour != 12:
            alarm_hour += 12

        while True:
            now = datetime.datetime.now()
            if alarm_hour == now.hour and alarm_min == now.minute:
                msg = MIMEText(data)
                msg['Subject'] = subject
                msg['From'] = EmailNotification.my_email
                msg['To'] = to

                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
                server.login(my_email, email_pass)
                server.send_message(msg)
                server.quit()
                # with smtplib.SMTP_SSL(EmailNotification.smtp_server, EmailNotification.smtp_port) as server:
                #     server.login(EmailNotification.my_email, EmailNotification.email_pass)
                #     server.send_message(msg)
                break




    def set_URL(self, alarm_hour: int, alarm_min: int, alarm_am: str, url:str):
        if alarm_am == "pm" and alarm_hour != 12:
            alarm_hour += 12
            
        while True:
            now = datetime.datetime.now()
            if alarm_hour == now.hour and alarm_min == now.minute:     
                # url= 'https://www.youtube.com/shorts/XoTl2b85o5U'  
                webbrowser.open_new_tab(url) 
                break
