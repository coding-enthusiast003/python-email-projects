from send_mails.send import Command  # Import the Command class from main.py
import getpass
from email.mime.base import MIMEBase  # Importing the MIMEBase class to create a base MIME type
from email import encoders  # Importing the encoders module
from email.mime.multipart import MIMEMultipart  # Importing the MIMEMultipart class to create a multipart message
from email.mime.text import MIMEText  # Importing the MIMEText class to create a text message
from rich.console import Console  # Importing the Console class from rich for better output formatting

class CommandWithAttachments(Command):
    """
    Extends the Command class to support file attachments.
    """
    def __init__(self):
        super().__init__()
        self.parser.add_argument(
            "-f", "--files", nargs="+", required=False, help="File paths to attach"
        )
        self.console  = Console()  # Create a Console object for rich output

    def add_attachments(self, msg, files):
        """
        Attach files to the email message.
        """
        for file_path in files:
            part = MIMEBase("application", "octet-stream")  # Create an instance of the MIMEBase class
            with open(file_path, "rb") as file:
                part.set_payload(file.read())  # Store file content in object

            encoders.encode_base64(part)  # Encode the payload in base64 format (encryption process)
            part.add_header(
                "Content-Disposition", f'attachment; filename="{file_path.split("/")[-1]}"'
            )  # Add the file name to the header
            msg.attach(part) # Attach the file to the message
        return msg

    def final_run(self):
        """
        Overrides the final_run method to include file attachments.
        """
        args = self.parser.parse_args()  # Parse the arguments

        # Prompt for the password securely if not provided in arguments
        password = self.console.input("[bold green]Please enter your email password (input will be hidden):[/bold green] ", password=True)  # Securely prompt for password

        # Set up the email with parsed arguments
        self.setup_message(
            sender=args.sender,
            password=password,
            receivers=args.receivers,
            subject=args.subject,
            body=args.body,
        )

        # Create a MIMEMultipart message for attachments
        msg = MIMEMultipart()
        msg["From"] = str(self.sender)
        msg["To"] = ", ".join(self.receivers)
        msg["Subject"] = args.subject
        msg.attach(MIMEText(args.body, "plain"))

        # Attach files if provided
        if args.files:
            msg = self.add_attachments(msg, args.files)

        # Send the email
        self.server_connection(msg)


if __name__ == "__main__":
    clu = CommandWithAttachments()  # Create an object of the CommandWithAttachments class
    clu.final_run()  # Call the final_run method to send the email