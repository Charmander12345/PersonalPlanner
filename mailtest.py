import email
import imaplib
import time

EMAIL = 'connor.jansen@alice.de'
PASSWORD = 'pupsi01'
SERVER = 'mail.o2online.de'

mail = imaplib.IMAP4_SSL(SERVER,993,timeout=10)
print(mail.login(EMAIL, PASSWORD))
mail.select('inbox')
status, messages = mail.search(None, 'ALL')
email_ids = messages[0].split()
if email_ids and status == "OK":
    time.sleep(1)
    try:
        mailstatus,message_data = mail.fetch(email_ids[0].decode(),"(RFC822)")
    except imaplib.IMAP4.abort as e:
        print(f"Verbindung abgebrochen: {e}")