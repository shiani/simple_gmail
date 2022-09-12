
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from mimetypes import guess_type as guess_mime_type
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode


class Message:

    def __init__(self, destination, subject, body, attachments=[]) -> None:
        self.destination = destination
        self.subject = subject
        self.body = body
        self.attachments = attachments

    @staticmethod
    def add_attachment(message, filename):
        content_type, encoding = guess_mime_type(filename)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(filename, 'rb')
            msg = MIMEText(fp.read().decode(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(filename, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(filename, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(filename, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(filename)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

    def build_message(self):
        if not self.attachments: # no attachments given
            message = MIMEText(self.body)
            message['to'] = self.destination
            message['from'] = "test26391@gmail.com"
            message['subject'] = self.subject
        else:
            message = MIMEMultipart()
            message['to'] = self.destination
            message['from'] = "test26391@gmail.com"
            message['subject'] = self.subject
            message.attach(MIMEText(self.body))
            for filename in self.attachments:
                self.add_attachment(message, filename)

        return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
    