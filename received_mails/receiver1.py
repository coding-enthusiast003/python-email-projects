import imaplib
import email
from email.header import decode_header
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
        self.connection = None  # Initialize connection attribute
         

     

    def user_details(self, username , password):
        self.username = username
        self.password = password
        return self.username, self.password

    def server_setup(self):
        try:
            # Connect to the IMAP server
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            # Ensure username and password are provided
            if not self.username or not self.password:
                raise ValueError("Username and password must not be None.")
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
        if not hasattr(self, 'connection') or self.connection is None:
            self.connection = self.server_setup()
            if not self.connection:
                raise Exception("Failed to establish connection.")
            self.console.print(f"[bold green]Logged in as: {self.username}[/bold green]")
        else:
            self.console.print(f"[bold cyan]Reusing existing connection, already logged in as {self.username}.[/bold cyan]")

        IDs = self.fetch_emailsID(self.connection)
        if not IDs:
            return  # Exit if no emails are found

        # Input validation for number of emails to fetch
        while True:
            num_input = self.console.input("[bold green]Enter the number of emails to fetch:[/bold green] ")
            if not num_input.strip():
                self.console.print("[bold red]Input cannot be empty. Please enter a number.[/bold red]")
                continue
            try:
                num = int(num_input)
                if num <= 0:
                    self.console.print("[bold red]Please enter a positive number.[/bold red]")
                    continue
                if num > len(IDs):
                    self.console.print("[bold red]Number exceeds total emails.[/bold red]")
                    continue
                break
            except ValueError:
                self.console.print("[bold red]Invalid input. Please enter a valid number.[/bold red]")

        self.console.print(f"[bold cyan]Fetching {num} emails...[/bold cyan]\n")
        for mail in sorted(IDs[-num:], reverse=True):
            # Fetch the email by ID
            status, msg_data = self.connection.fetch(mail, "(RFC822)")

            # Parse the email content safely
            if msg_data and isinstance(msg_data[0], tuple) and isinstance(msg_data[0][1], (bytes, bytearray)):
                msg = email.message_from_bytes(msg_data[0][1])  # Convert bytes to string
            else:
                self.console.print(f"[bold red]Failed to fetch or parse email with ID {mail.decode('utf-8')}.[/bold red]")
                continue

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
            self.connection.store(mail.decode('utf-8'), "+FLAGS", "\\Seen")
            self.console.print("[bold green]Email marked as read.[/bold green]\n")
            
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
            
             
            self.fetch_mails() #calling the fetch_mails method from parent class to fetch the emails

            if self.connection:  # Only logout if connection exists
                self.connection.logout()  # Logout from the email server
                self.console.print("[bold green]Logged out successfully![/bold green]") #printing this message for debugging purpose
            else:
                self.console.print("[bold yellow]No active connection to logout.[/bold yellow]")
        except KeyboardInterrupt:
            self.console.print("[bold red]Program interrupted by user.[/bold red]")
        except SystemExit:
            self.console.print("[bold red]Program exited.[/bold red]")    
        except Exception as e:
            self.console.print(f"[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    cli = CommandInterface() #creating an object of the Command class
    cli.final_run() #calling the final_run method to execute the program











