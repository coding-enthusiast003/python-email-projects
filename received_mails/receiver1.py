import imaplib
import email
from email.header import decode_header
import getpass
import argparse

 

class EmailReceiver:
    def __init__(self):
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993
        self.username = None
        self.password = None
         

    def user_details(self,username,password):
        self.username=  username
        self.password = password
        

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
        try:
            # Fetch all emails in the inbox
            status, messages = mail.search(None, "ALL")

            if status != "OK" or not messages[0]:
                print("No emails found.")
                return []
            
            email_ids = messages[0].split()
            print(f"Total emails: {len(email_ids)}\n")
            return email_ids
        
        except Exception as e:
            print(f"An error occurred while fetching emails: {e}")
            return []

    
    def fetch_mails(self):
        # Iterate through the email IDs and fetch each email
        connection = self.server_setup()

        IDs = self.fetch_emailsID(connection)
        if not IDs:
            return  # Exit if no emails are found

        num = int(input("Enter the number of emails to fetch: "))
        if num > len(IDs):
            print("Number exceeds total emails.")
            return
        print(f"Fetching {num} emails...\n")
        for mail in sorted(IDs[-num:], reverse=True):
            # Fetch the email by ID
            status, msg_data = connection.fetch(mail, "(RFC822)")

            # Parse the email content
            msg = email.message_from_bytes(msg_data[0][1])  # Convert bytes to string

            subject_data = msg["Subject"]  # Store subject first
            if subject_data is None:
                subject, encoding = "(No Subject)", None
            else:
                subject, encoding = decode_header(subject_data)[0]

            if isinstance(subject, bytes):  # Check if subject is in bytes
                # If it's in bytes, decode to str using the detected encoding or default to utf-8 
                subject = subject.decode(encoding if encoding else "utf-8")

             
            # Print email details
            print(f"Email ID: {mail.decode('utf-8')}")
            print(f"From: {msg['From']}")
            print(f"Subject: {subject}")
            print(f"Date: {msg['Date']}\n")
            print(80 * "-")
            connection.store(mail.decode('utf-8'), "+FLAGS", "\\Seen")
            print("Email marked as read.\n")
            
        connection.logout()
        print("Emails fetched successfully!")

 
class CommandInterface(EmailReceiver): #Inheriting from EmailReceiver class
    def __init__(self):
        super().__init__() #Initializing the parent properties
        self.parser = argparse.ArgumentParser(
            description="Welcome to the email command prompt")  #creating an argument parser object
        self.parser.add_argument(
            "-u", "--username", required=True, help="Enter your email address")
        self.parser.add_argument(
            "-p", "--password", help="Enter your email password")

    def final_run(self):
        try:
            args = self.parser.parse_args()  #parse the arguments

        # Use the provided password or prompt for it securely
            self.password = args.password if args.password else getpass.getpass("Please enter your email password (input will be hidden): ")

            # Set up the email receiver with the provided username and password
            self.user_details(
                username=args.username,
                password=self.password
            )
            self.fetch_mails()
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    cli = CommandInterface() #creating an object of the Command class
    cli.final_run() #calling the final_run method to execute the program











