import imaplib
import email
from email.encoders import decode_header
import getpass
import argparse
from receiver1 import EmailReceiver, CommandInterface


class EmailReceiver2(EmailReceiver): # Inheriting from EmailReceiver class
    def __init__(self):
        super().__init__()

    def fetch_mails(self): # Overriding the fetch_mails method from EmailReceiver class
        connection = self.server_setup() # Calling server_setup method from EmailReceiver class

        IDs = self.fetch_emailsID(connection) # Calling fetch_emailsID method from EmailReceiver class to fetch email IDs
        if not IDs:
            return  # Exit if no emails are found
        
        num = int(input("Enter the number of emails to fetch: "))
        if num > len(IDs):
            print("Number exceeds total emails.")  # Check if the number exceeds total emails
            return
        print(f"Fetching {num} emails...\n")
        for mail in sorted(IDs[-num:], reverse=True):
            # Fetch the email by ID
            status, msg_data = connection.fetch(mail, "(RFC822)")

            # Parse the email content
            msg = email.message_from_bytes(msg_data[0][1])  # Convert bytes to string
            subject, encoding = decode_header(msg["Subject"])[0]  # Decode the email subject

            if isinstance(subject, bytes):  # Check if subject is in bytes
                # If it's in bytes, decode to str using the detected encoding or default to utf-8 
                subject = subject.decode(encoding if encoding else "utf-8")
            # Print email details
            print(f"Email ID: {mail.decode('utf-8')}")
            print(f"From: {msg['From']}")
            print(f"Subject: {subject}")
            print(f"Date: {msg['Date']}\n")

            # Extract and print full body
            body = self.extract_body(msg)
            print(f"\nBody:\n{body}\n")

            print(80 * "-") # Print a separator line
            # Mark the email as read (optional)
            connection.store(mail, "+FLAGS", "\\Seen")
            
        connection.logout()
        print("Emails fetched successfully!")