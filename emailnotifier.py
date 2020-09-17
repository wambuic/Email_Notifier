from email import encoders#responsible for encryption of data
from email.mime.base import MIMEBase# is used for fetching of the API
from email.mime.multipart import MIMEMultipart#
from email.mime.text import MIMEText#mod
import base64#delude the encryption
import os#importing the operating system
def create_message(sender, to, subject, message_text):
  """Create a message for an email.
Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
Returns:
    An object containing a base64url encoded email object.
    so that one cannot eavesdrop or tap
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
def send_message(service, user_id, message):

      """Send an email message.
Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
Returns:
    Sent Message.
  """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
        print('Message Id: {}'.format(message['id']))
        return message
    except:
        print ('An error occurred')

def notification(sender, to, subject, notification):
    #Sender is the sender email, to is the receiver email, subject is the email subject, and notification is the email body message. All the text is str object.
    SCOPES = 'https://mail.google.com/'
    message = create_message(sender, to, subject, notification)
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        #We use login if no valid credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow =   InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    send_message(service, sender, message) 