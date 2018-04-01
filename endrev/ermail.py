import email
import smtplib
import hashlib

from email.MIMEMultipart import MIMEMultipart

import mailinfo

HASHFILE = "/var/www/endrev/endrev/data/mail.hash"

def send(subject, body):
    msg = "Subject: %s\n\n%s" % (subject, body)
    hash = hashlib.md5(msg).hexdigest()

    try:
        with open(HASHFILE, 'r') as f:
            hashlist = [line.strip() for line in f.read().split('\n')]
    except IOError:
        return -1 

    if hash in hashlist: return 1
    hashlist.append(hash)

    try:
        mail = smtplib.SMTP_SSL(mailinfo.SERVER, mailinfo.PORT)
        mail.ehlo()
        mail.login(mailinfo.USERNAME, mailinfo.PASSWORD)
        mail.sendmail(mailinfo.USERNAME, mailinfo.USERNAME, msg)
        mail.quit()
    except email.errors.MessageError:
        return -1

    try: 
        with open(HASHFILE, 'w') as f:
            f.write('\n'.join(hashlist))
    except IOError:
        return 1

    return 0
