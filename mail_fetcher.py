import smtplib
import time
import imaplib
import email
import traceback
import json

def mail_create(mailaddres,pw,author):

    latestmail = gatherMail(mailaddres, pw)

    try:

        cassio = open("database.json", "r")
        db = json.load(cassio)
        cassio.close()

        #db[author] = {"creds": ["try", "again"], "mailhistory": maillist}
        db = {author: {"creds": [mailaddres, pw], "mailhistory": latestmail}}

        cassio = open("database.json", "w")
        json.dump(db, cassio)
        cassio.close()


        return 200

    except Exception as e:
        traceback.print_exc() 
        return(str(e))

def gatherMail(mailaddres, pw):

    FROM_EMAIL = mailaddres
    FROM_PWD = pw
    SMTP_SERVER = "imap.gmail.com" 
    SMTP_PORT = 993

    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
    mail.select('inbox')

    data = mail.search(None, 'ALL')
    mail_ids = data[1]
    id_list = mail_ids[0].split()   
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    latestmail = []

    for i in range(latest_email_id,first_email_id, -1):
        data = mail.fetch(str(i), '(RFC822)' )
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1], "utf-8"))
                email_subject = msg['subject']
                email_from = msg['from']
                
                if not latestmail:
                    latestmail = [email_subject, email_from]

    return latestmail