#!/usr/bin/python3

from base64 import b64encode, b64decode
from logger import Logger
from util import getAbsolutePath
from sendgrid.helpers.mail import Email, Mail, Content, Attachment, Personalization
import sendgrid
import os


def sendlog():

    sg = sendgrid.SendGridAPIClient(apikey=os.environ['SENDGRID_API_KEY'])

    contentString = "bi-weekly refactoring roundup"

    attachment = Attachment()
    attachment.content = encodefile('log/out.txt')
    attachment.type = 'text/plain'
    attachment.filename = 'log/out.txt'
    attachment.disposition = 'attachment'
    attachment.content_id = 'log'

    from_email = Email('zach@refactorcamp.org')
    to_email = Email('vgururao@gmail.com')
    subject = 'refactoring roundup'
    content = Content('text/plain', contentString)
    mail = Mail(from_email, subject, to_email, content)
    mail.add_attachment(attachment)
    mail.personalizations[0].add_cc(Email('zach@zfadd.is'))
    
    response = sg.client.mail.send.post(request_body=mail.get())
    
    print(response.status_code)
    print(response.body)
    print(response.headers)


def encodefile(filePath):
    with open(filePath, 'rb') as file:
        fileString = file.read()

    encoded_fileString = b64encode(fileString)

    return encoded_fileString.decode()


if __name__ == '__main__':
    logDir = getAbsolutePath(__file__, 'log/')
    logfile = 'out.txt'
    logger = Logger(logDir, logfile)
    sendlog()
    logger.archive()


