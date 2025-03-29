import imaplib
import email
from email.header import decode_header
import getpass

class EmailReceiver:
    def __init__(self):
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993
        self.username = None
        self.password = None
         

    def user_details(self):
        self.username= input("Enter your email: ")
        self.password = getpass.getpass("Enter your password: ")

    def server_setup(self):
        try:
            # Connect to the IMAP server
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            # Login to your account
            mail.login(self.username, self.password)
            mail.select('inbox')  # Select inbox folder

            return mail
        
        except imaplib.IMAP4.error as e:
            print(f"Failed to connect to the server: {e}")
    
    def fetch_emailsID(self, mail):
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()

        print(f"Total emails: {len(email_ids)}\n")
        return email_ids
    
    def fetch_mails(self):
        # Iterate through the email IDs and fetch each email
        connection = self.server_setup()
        IDs = self.fetch_emailsID(connection)
        num = int(input("Enter the number of emails to fetch: "))
        if num > len(IDs):
            print("Number exceeds total emails.")
            return
        print(f"Fetching {num} emails...\n")
        for mail in sorted(IDs[-num:],reverse = True):

            # Fetch the email by ID

            status, msg_data = connection.fetch(mail, "(RFC822)")

            # Parse the email content

            msg = email.message_from_bytes(msg_data[0][1]) #convert bytes to string
            subject, encoding = decode_header(msg["Subject"])[0]  # Decode the email subject

            if isinstance(subject, bytes): # check if subject is in bytes
                # If it's in bytes, decode to str using the detected encoding or default to utf-8 
                subject = subject.decode(encoding if encoding else "utf-8")
            # Print email details
            print(f"Email ID: {mail.decode('utf-8')}")
            print(f"From: {msg['From']}")
            print(f"Subject: {subject}")
           
            print(f"Date: {msg['Date']}\n")
            
            print(50 * "-")
            connection.store(mail, "+FLAGS", "\\Seen")
            
        connection.logout()
        print("Emails fetched successfully!")

receiver = EmailReceiver()
receiver.user_details()
receiver.fetch_mails()
 

           
        


    