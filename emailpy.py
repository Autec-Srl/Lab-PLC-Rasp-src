import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

def SendMail(   username = "giampiero.novello@office365.com",
        password = "Autec2025!",
        mail_from = "   AS000TST@autecsafety.com",
        mail_to = "giuliano.cristofoli@autecsafety.com",
        mail_subject = "Test in esecuzione ",
        mail_body = "This is a test message"):
    #smtplib.SMTP.set_debuglevel(2)
    mimemsg = MIMEMultipart()
    mimemsg['From']=mail_from
    mimemsg['To']=mail_to
    mimemsg['Subject']=mail_subject
    mimemsg.attach(MIMEText(mail_body, 'plain'))
    connection = smtplib.SMTP(host='10.16.0.10', port=25)
    connection.send_message(mimemsg)
    connection.quit()

def main():
    i=0
    while(i<100):
        SendMail()
        time.sleep(1)
        print(i)
        i=i+1

if __name__ == '__main__':
    main()
