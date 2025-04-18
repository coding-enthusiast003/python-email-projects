import imaplib
import email
from email.header import decode_header
import getpass
import argparse
import rich
from rich.console import Console
 

class EmailReceiver:
    def __init__(self):
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993
        self.username = None
        self.password = None
        self.console = Console()  # Creating an instance of Console for rich text output
         

     

    def user_details(self, username , password):
        self.username = username
        self.password = password
        return self.username, self.password

    def server_setup(self):
        try:
            # Connect to the IMAP server
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            # Login to your account
            mail.login(self.username, self.password)
            mail.select('inbox')  # Select inbox folder
             

            return mail
        
        except imaplib.IMAP4.error as e:
            self.console.print(f"[bold red]Failed to connect to the server: {e}[/bold red]")
    
    def fetch_emailsID(self, mail):
        try:
            # Fetch all emails in the inbox
            status, messages = mail.search(None, "ALL")

            if status != "OK" or not messages[0]:
                self.console.print("[bold red]No emails found.[/bold red]")
                return []
            
            email_ids = messages[0].split()
            self.console.print(f"[bold cyan]Total emails: {len(email_ids)}[/bold cyan]\n")
            return email_ids
        
        except Exception as e:
            self.console.print(f"[bold red]An error occurred while fetching emails: {e}[/bold red]")
            return []

    
    def fetch_mails(self):
        # Iterate through the email IDs and fetch each email
        connection = self.server_setup()
        if not connection:
            raise Exception("Failed to establish connection.")
        self.console.print("[bold green]Connected to the email server successfully![/bold green]")

        IDs = self.fetch_emailsID(connection)
        if not IDs:
            return  # Exit if no emails are found

        num = int(self.console.input("[bold green]Enter the number of emails to fetch:[/bold green] "))
        if num > len(IDs):
            self.console.print("[bold red]Number exceeds total emails.[/bold red]")
            return
        self.console.print(f"[bold cyan]Fetching {num} emails...[/bold cyan]\n")
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
            self.console.print(f"[bold yellow]Email ID:[/bold yellow] {mail.decode('utf-8')}")
            self.console.print(f"[bold yellow]From:[/bold yellow] {msg['From']}")
            self.console.print(f"[bold yellow]Subject:[/bold yellow] {subject}")
            self.console.print(f"[bold yellow]Date:[/bold yellow] {msg['Date']}\n")
            self.console.print(f"[bold magenta]{80 * '-'}[/bold magenta]")
            connection.store(mail.decode('utf-8'), "+FLAGS", "\\Seen")
            self.console.print("[bold green]Email marked as read.[/bold green]\n")
            
        connection.logout()
        self.console.print("[bold green]Emails fetched successfully![/bold green]")

 
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
            self.password = args.password if args.password else self.console.input("[bold green]Please enter your email password (input will be hidden):[/bold green] ", password=True)

            # Set up the email receiver with the provided username and password
            self.user_details(
                username=args.username, password=self.password
                )  #setting the user details
            
            self.console.print(f"[bold green]Logged in as: {self.username}[/bold green]")
            self.fetch_mails()
        except Exception as e:
            self.console.print(f"[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    cli = CommandInterface() #creating an object of the Command class
    cli.final_run() #calling the final_run method to execute the program











