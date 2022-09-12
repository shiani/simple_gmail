
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from mimetypes import guess_type as guess_mime_type
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
import os

class Message:
    """Message Class creates an message object to send with mail service.
    Args:
        From : a name that you want to show in email sender.
        To: destination of your message.
        subject: subject of your message.
        body: body text of your message.
        attachments: list of atachments paths

    """
    def __init__(self,From: str, To: str, subject: str, body: str, attachments=[]) -> None:
        self.To = To
        self.From = From
        self.subject = subject
        self.body = body
        self.attachments = attachments
        

    @staticmethod
    def add_attachment(message, filename) ->None:
        content_type, encoding = guess_mime_type(filename)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)

        with open(filename, 'rb') as fp:
            if main_type == 'text':
                msg = MIMEText(fp.read().decode(), _subtype=sub_type)
            elif main_type == 'image':
                msg = MIMEImage(fp.read(), _subtype=sub_type)
            elif main_type == 'audio':
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
            else:
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(fp.read())
            fp.close()

        filename = os.path.basename(filename)
        # add headers
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

    def build_message(self) -> dict:
        message = MIMEMultipart()
        message['to'] = self.To
        message['from'] = self.From
        message['subject'] = self.subject
        message.attach(MIMEText(self.body))
        if self.attachments: 
            for filename in self.attachments:
                self.add_attachment(message, filename)

        return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
    