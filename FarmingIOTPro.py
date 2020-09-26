#------------------------------------------------------------------------  FARMING   ---------------------------------------------------------------------------#
#---------------------------------------------------------Getting water level and detecting the soil moisture--------------------------------------------------#
import RPi.GPIO as GPIO
import time
#import yagmail
import smtplib,ssl
#import smtpemail
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = ""  # Enter your address
receiver_email = ""  # Enter receiver address
password =" "  #input("Type your password and press enter: ")
message = """\
Subject:  NO MOISTURE

Restart the System .NO MOISTURE IN THE SOIL. START THE SPRINKLERS"""
context = ssl.create_default_context()

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
TRIG=35
ECHO=40
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(11,GPIO.IN)
GPIO.setup(31,GPIO.OUT)
iv=0
start=0
end=0
distance=0
GPIO.output(TRIG,False)
time.sleep(2)
GPIO.output(TRIG,True)
time.sleep(0.00001)
GPIO.output(TRIG,False)
while(GPIO.input(ECHO)==0):
    start=time.time()
while(GPIO.input(ECHO)==1):
    end=time.time()
sig_time=end-start
distance=sig_time*17150
distance=round(distance,2)
print("Distance:"+str(distance))
pin=11
while(1):
	iv=GPIO.input(pin)
	time.sleep(0.5)
	if(iv==0):
		print("MOIST")
		GPIO.output(31,GPIO.LOW)
	else:
		print("NOPE[!]")
		GPIO.output(31,GPIO.HIGH)
		s=smtplib.SMTP('smtp.gmail.com',587)
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login(sender_email,password)
		s.sendmail(sender_email,receiver_email,message)
		s.quit()
#	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#    			server.login(sender_email, password)
#   			server.sendmail(sender_email, receiver_email, message)
		print("[!] NO MOISTURE RESTART THE SYSTEM [!] ")
#		break
GPIO.cleanup()
