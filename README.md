 
# Simple Gmail

This is a Gmail Task for Haensel AMS RecruitingTeam


## Installation

Install requierments with pip

```bash
  pip install -r requierments.txt
```

This module is using Gmail API so first we need to get cred.json file from google.
To use the Gmail API, we need to connect to Gmail's API. We can get one from [Google API Dashboard](https://console.developers.google.com/apis/dashboard)

We first need to enable Gmail Api, go to dashboard and use search bar for Gmail API, then enable it.

Then create an OAuth 2.0 client ID by creating credentials(by + CREATE CREDENTIALS)

click on OAuth client ID.

Select Desktop app.

Then download the json.

Copy the file in your main.py app file path.


## Usage/Examples


For sending email by your gmail:

```python
from simple_gmail.mail import Gmail
from simple_gmail.message import Message


# create an instance of Gmail, if everything is ok, you are authenticated here
g = Gmail()

# create 
m = Message(From='your name', To="destination@example.com", subject="some subject", body="some body", attachments=['/root/to/attachment1', '/root/to/attachment2'])

# send your mail
g.send_mail(m)

```

For searching in email INBOX and SENTBOX:

```python
from simple_gmail.mail import Gmail
from simple_gmail.message import Message


# create an instance of Gmail, if everything is ok, you are authenticated here
g = Gmail()

# you can search by search_mail
result = g.search_mail("your query")
print(result)
```
