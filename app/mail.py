

from django.core.mail import EmailMessage
import threading


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, to=self.recipient_list)
        msg.send()


def send(subject, body, mail):

    to_mail = mail
    if isinstance(mail, str):
        to_mail = [mail]
    try:
        EmailThread(subject, body, to_mail).run()
    except:
        pass
