
#!/usr/bin/env python

from base64 import urlsafe_b64decode
import email
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build



class SendMail:

    def __init__(self, service) -> None:
        self.service = service    
    
    def send_mail(self, message):
        return self.service.users().messages().send(userId='me', body= message.build_message()).execute()


class SearchMail:

    def __init__(self, service) -> None:
        self.service = service

    @staticmethod
    def get_size_format(b, factor=1024, suffix="B"):
        """
        Scale bytes to its proper byte format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}{unit}{suffix}"
            b /= factor
        return f"{b:.2f}Y{suffix}"
    
    def search_by_query(self, query):
        result = self.service.users().messages().list(userId='me', q=query).execute()
        # print(result)
        mail_list = list()
        if result.get('messages', None):
            for item in result['messages']:
                # grab the message instance
                message = self.service.users().messages().get(userId='me', id=item['id'],format='raw').execute()
                # decode the raw string, ASCII works pretty well here
                msg_str = urlsafe_b64decode(message['raw'].encode('ASCII'))

                # grab the string from the byte object
                mime_msg = email.message_from_bytes(msg_str)
                # there will usually be 2 parts the first will be the body in text
                # the second will be the text in html
                parts = mime_msg.get_payload()
                # return the encoded text
                final_content = parts[0]
                
                mail = dict()
                mail['LabelIds'] = message['labelIds'][0]
                mail['Subject'] = mime_msg['Subject']
                mail['From'] = mime_msg['From']
                mail['To'] = mime_msg['To']
                mail['Date'] = mime_msg['Date']
                mail['Attachments'] = []
                msg = self.service.users().messages().get(userId='me', id=item['id'], format='full').execute()
                payload = msg['payload']
                # headers = payload.get("headers")
                ps = payload.get("parts")
                
                

                # create folder for attachment
                current_path = os.getcwd()
                if not os.path.isdir('attachments'):
                    os.mkdir("attachments")
                os.chdir("attachments")
                folder_name = f"./{mail['LabelIds']}/{mail['Date'][5:-6]}"
                if not os.path.isdir(folder_name):
                    if not os.path.isdir(f"./{mail['LabelIds']}"):
                        os.mkdir(f"./{mail['LabelIds']}")
                    os.chdir(f"./{mail['LabelIds']}")
                    os.mkdir(f"{mail['Date'][5:-6]}")
                    os.chdir(f"{mail['Date'][5:-6]}")
                    file_path = os.getcwd()
                    os.chdir(current_path)

                for part in ps:
                    part_headers = part.get("headers")
                    body = part.get("body")
                    filename = part.get("filename")

                    for part_header in part_headers:
                        part_header_name = part_header.get("name")
                        part_header_value = part_header.get("value")
                        if part_header_name == "Content-Disposition":
                            if "attachment" in part_header_value:
                                # we get the attachment ID 
                                # and make another request to get the attachment itself
                                attachment_id = body.get("attachmentId")
                                attachment = self.service.users().messages() \
                                            .attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                                data = attachment.get("data")
                                filepath = os.path.join(file_path, filename)
                                if data:
                                    with open(filepath, "wb") as f:
                                        f.write(urlsafe_b64decode(data))
                                        mail['Attachments'].append(f'{filepath}')

                # this is because of the diffrence between sentbox and mailbox
                if len(final_content.get_payload()[0]) > 1:
                    mail['Body'] = final_content.get_payload()[0].get_payload().strip()
                else:
                    mail['Body'] = final_content.get_payload()
                

                mail_list.append(mail)

        return mail_list

class Gmail:
    def __init__(self) -> None:
        self._cred = None
        self._scopes = ['https://mail.google.com/']
        self.__authenticate__()


    def __authenticate__(self) -> None:
        # if user has credentials
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self._cred = pickle.load(token)

        # if there are no (valid) credentials availablle, let the user log in.
        if not self._cred or not self._cred.valid:
            if self._cred and self._cred.expired and self._cred.refresh_token:
                self._cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('cred.json', self._scopes)
                self._cred = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(self._cred, token)
        self.service = build('gmail', 'v1', credentials=self._cred)


    def send_mail(self, message):

        return SendMail(self.service).send_mail(message)
    
    def search_mail(self, query: str):

        return SearchMail(self.service).search_by_query(query)


