from send_mails.send2 import CommandWithAttachments as cmd   # Import the CommandWithAttachments class from send2.py
from send_mails.send import Emailsender  # Import the Command class from main.py
from rich.console import Console #importing the console class from rich for better output formatting
from email.mime.base import MIMEBase  # Importing the MIMEBase class to create a base MIME type
from email import encoders  # Importing the encoders module
from email.mime.multipart import MIMEMultipart  # Importing the MIMEMultipart class to create a multipart message
from email.mime.text import MIMEText  # Importing the MIMEText class to create a text message
from send_mails.utility import * # Importing the utility module for utility functions


class FinalCommand(cmd, Emailsender):
    """
    A class that combines the functionality of sending emails with attachments and the base email sending functionality.
    It inherits from CommandWithAttachments and Emailsender to utilize their methods and attributes.
    """
    
    def __init__(self):
        cmd.__init__(self)  # Initialize CommandWithAttachments
        Emailsender.__init__(self)  # Initialize Emailsender
        self.console = Console()  # Create a Console object for rich output
        self.msg = None  # Initialize msg to None
        self.sender = None
        self.password = None
        self.receivers = []
        # self.parser.add_argument("-f", "--files", nargs="+", required=False, help="File paths to attach")


    def final_output(self):
        args = self.parser.parse_args()  # Parse the arguments
        try:

            self.sender = args.sender  # Prompt for sender email if not provided

            if args.receivers:
                # If receivers is a string, split it; if it's already a list, use as is
                if isinstance(args.receivers, str):
                    self.receivers = [email.strip() for email in args.receivers.split(",")]
                else:
                    self.receivers = [email.strip() for email in args.receivers]
            else:
                self.receivers = [email.strip() for email in self.console.input("[bold green]Please enter receiver's email addresses (comma-separated):[/bold green] ").split(",")]  # Prompt for receiver emails if not provided

            

            self.password = self.console.input("[bold green]Please enter your email password (input will be hidden):[/bold green] ", password=True)  # Securely prompt for password

            self.subject = args.subject if args.subject else self.console.input("[bold green]Please enter the subject of your email:[/bold green] ")  # Get the subject of the email

            self.body = args.body if args.body else self.console.input("[bold green]Please enter the body of your email:[/bold green] ")  # Prompt for body if not provided

            self.setup_message(  # Set up the email with parsed arguments
                sender=self.sender,
                password=self.password,
                receivers=self.receivers,
                subject=self.subject,
                body=self.body
            )
            # Create a MIMEMultipart message for attachments
            msg = MIMEMultipart()
            msg["From"] = str(self.sender)
            msg["To"] = ", ".join(self.receivers)
            msg["Subject"] = self.subject
            msg.attach(MIMEText(self.body, "plain"))

            # If files are provided, add them as attachments
            files = self.console.input("[bold green]DO you want to attach files? (yes/no):[/bold green]").strip().lower()
            try:
                if files == "yes":
                    args.files = args.files 
                    if args.files:
                        msg = self.add_attachments(msg, args.files)
                    else:
                        self.console.print("[bold red]No files provided for attachment.[/bold red]")

            except Exception as e:
                self.console.print(f"[bold red]Error occurred while adding attachments: {e}[/bold red]")
            
            # send the mail 
            self.server_connection(msg)  # Send the email

        except FileNotFoundError as fnf_error:
            self.console.print(f"[bold red]File not found: {fnf_error}[/bold red]")
            return

        except ValueError as ve:
            self.console.print(f"[bold red]Value Error: {ve}[/bold red]")
            return
        except KeyboardInterrupt:
            self.console.print("[bold red]Operation cancelled by user.[/bold red]")
            return
        except Exception as e:
            self.console.print(f"[bold red]Failed to set up email: {e}[/bold red]")
            return

if __name__ == "__main__":
    command = FinalCommand()  # Create an object of the FinalCommand class
    command.final_output()  # Call the final_output method to send the email