import argparse      #importing the argparse module for command line arguments
import smtplib as s  #importing the smtplib module for sending emails
import getpass       #importing the getpass module for secure password input
from rich.console import Console  # Importing the Console class from rich for better output formatting
from send_mails.utility import *  # Importing utility functions from the utility module

class Emailsender:
    """
    A class to send emails using an SMTP server.
    Attributes:
        smtp_server (str): The SMTP server address. Defaults to "smtp.gmail.com".
        smtp_port (int): The port number for the SMTP server. Defaults to 587.
        sender (str): The email address of the sender.
        password (str): The password for the sender's email account.
        receivers (list): A list of recipient email addresses.
        message (str): The email message to be sent.
    Methods:
        __init__(smtp_server="smtp.gmail.com", smtp_port=587):
            Initializes the Emailsender instance with default or provided SMTP server and port.
        setup_message(sender, password, receivers, subject, body):
            Configures the sender's credentials, recipient email addresses, and the email content.
        server_connection():
            Establishes a connection to the SMTP server, logs in, and sends the email to the recipients.
    """
     
 
    
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender = None 
        self.password = None
        self.receivers = []
        self.message = None
        self.console = Console()  # Create a Console object for rich output

    def setup_message(self, sender, password, receivers, subject, body):
        self.sender = sender
        self.password = password
        # Accept both comma-separated string and list for receivers
        if isinstance(receivers, str):
            self.receivers = [email.strip() for email in receivers.split(",")]
        elif isinstance(receivers, list):
            self.receivers = [email.strip() for email in receivers]
        else:
            self.receivers = []
        self.message = f"Subject: {subject}\n\n{body}"
        return self.sender, self.password, self.receivers, self.message

    def server_connection(self, msg=None):
        try:
            if self.sender is None or self.password is None:
                raise ValueError("Sender email and password must not be None.")
            if msg is None and self.message is None:
                raise ValueError("Email message must not be None.")

            with s.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()    #start the TLS connection for secure communication
                connect = server.login(str(self.sender), str(self.password))    #login to the email account
                if connect:
                    ui() #calling the ui function to print the user interface
                    self.console.print(f"Connected to {self.smtp_server} as {self.sender}", style="bold green")
                # If a MIMEMultipart message is provided, send it
                if msg:
                    for receiver in self.receivers:
                        server.sendmail(str(self.sender), receiver, msg.as_string())
                        self.console.print(f"Email sent successfully to {receiver}!", style="bold green")
                else:
                    for receiver in self.receivers:
                        server.sendmail(str(self.sender), receiver, str(self.message))   #send the email
                        self.console.print(f"Email sent successfully to {receiver}!", style="bold green")
        except s.SMTPAuthenticationError:
            self.console.print("Authentication failed. Please check your email and password.", style="bold red")
            return
        except Exception as e:
            self.console.print(f"Failed to send email: {e}", style="bold red")
            return


class Command(Emailsender):
    """
    A command-line interface for sending emails using the Emailsender class.
    This class provides a command-line tool to send emails by parsing arguments 
    such as sender email, receiver email(s), subject, and body. It securely 
    prompts for the sender's email password if not provided.
    Methods:
        __init__():
            Initializes the Command class, sets up the argument parser, and 
            defines the required arguments for sending an email.
        final_run():
            Parses the command-line arguments, securely prompts for the sender's 
            email password, sets up the email message, and sends the email.
    """

    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(description="Welcome to the email command prompt")  #creating an argument parser object
        self.parser.add_argument("-s","--sender",  help="Enter your email address")
        self.parser.add_argument("-r","--receivers", 
                                 help="Enter receiver email addresses ")
        self.parser.add_argument("-t","--subject",  help="Enter the subject")
        self.parser.add_argument("-b","--body",  help="Enter the body of your email")

    def final_run(self):
        args = self.parser.parse_args()  #parse the arguments

        # Prompt for the password securely if not provided in arguments
        password = getpass.getpass("Please enter your email password (input will be hidden): ")

        # Set up the email with parsed arguments
        self.setup_message(
            sender=args.sender,
            password=password,
            receivers=args.receivers,
            subject=args.subject,
            body=args.body
        )

        # Send the email
        self.server_connection()


if __name__ == "__main__":
    clu = Command() #creating an object of the Command class
    clu.final_run() #calling the final_run method to send the email
