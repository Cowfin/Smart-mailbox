import smtplib
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
GMAIL_USERNAME = '@gmail.com'
GMAIL_PASSWORD = ''

RECIPIENT = "@gmail.com"


def sendmail(content):

    subject = "New mail detected"
    content = str(time.ctime()) + " " + content

    # Create Headers
    emailData = MIMEMultipart()
    emailData['Subject'] = subject
    emailData['To'] = RECIPIENT
    emailData['From'] = GMAIL_USERNAME
    emailData.attach(MIMEText(content))

    imageData = MIMEImage(open('mailbox.png', 'rb').read(), 'png')
    imageData.add_header('Content-Disposition',
                         'attachment; filename="mailbox.png"')
    emailData.attach(imageData)

    # Connect to Gmail Server
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()

    # Login to Gmail
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    # Send Email & Exit
    session.sendmail(GMAIL_USERNAME, RECIPIENT, emailData.as_string())
    session.quit
