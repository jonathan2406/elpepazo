from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# By gpt
class Notifications:
    def __init__(self,from_address=None, password=None):
        if None in [from_address]:
            self.from_address = "dnjervicenotifications@gmail.com"
            self.password = "yhws dgnc pvey fbdl"
        else:
            self.from_address = from_address    
            self.password = password


    def send_email(self, to_address, subject, message):
        msg = MIMEMultipart()
        
        msg['From'] = self.from_address
        msg['To'] = to_address
        msg['Subject'] = "New appointment scheduled!"
        
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        server.login(self.from_address, self.password)
        
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()