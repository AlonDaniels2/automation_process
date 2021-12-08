import glob
import smtplib
import os
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
import datetime
import log_funcs
import sys

def send_email():
    """Send email of the last csv file in \\Downloads.
    """

    # Dates for email topic
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=7)
    a_week_ago = today - delta

    from_addr = 'source_email_address'
    to_addr = 'destination_address'
    subject = 'RecordList ' + a_week_ago.strftime("%d/%m/%Y") + ' - ' + today.strftime("%d/%m/%Y")
    body = 'No pain, no gain!'
    pw = 'your_email_password'

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = from_addr

    # storing the receivers email address
    msg['To'] = to_addr

    # storing the subject
    msg['Subject'] = subject

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    try:
        # open the file to be sent
        folder_path = r'F:\Downloads'
        file_type = '\*csv'
        files = glob.glob(folder_path + file_type)
        filename = max(files, key=os.path.getctime)
    except Exception as e:
        log_funcs.log_error(e)
        sys.exit()

    attachment = open(filename, "rb")

    # Instance of MIMEBase and named as p.
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form.
    p.set_payload((attachment).read())

    # Encode into base64.
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # Attach the instance 'p' to instance 'msg'.
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # Start TLS for security.
    s.starttls()

    # Authentication.
    s.login(from_addr, pw)

    # Convert the Multipart msg into a string.
    text = msg.as_string()

    # Send the mail.
    s.sendmail(from_addr, to_addr, text)

    # Terminate the session.
    attachment.close()
    s.quit()