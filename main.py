import argparse      #importing the argparse module for command line arguments
import smtplib as s  #importing the smtplib module for sending emails
import getpass       #importing the getpass module for secure password input


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

    def setup_message(self, sender, password, receivers, subject, body):
        self.sender = sender
        self.password = password
        self.receivers = [email.strip() for email in receivers.split(",")]
        self.message = f"Subject: {subject}\n\n{body}"

    def server_connection(self,msg=None):
        try:
            with s.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()    #start the TLS connection for secure communication
                server.login(self.sender, self.password)    #login to the email account

                # If a MIMEMultipart message is provided, send it
                if msg:
                    for receiver in self.receivers:
                        server.sendmail(self.sender, receiver, msg.as_string())
                        print(f"Email with attachment sent successfully to {receiver}!")
                else:
                    for receiver in self.receivers:
                        server.sendmail(self.sender, receiver, self.message)   #send the email
                        print(f"Email sent successfully to {receiver}!")

        except Exception as e:
            print(f"Failed to send email: {e}")


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
        self.parser.add_argument("-s","--sender", required=True, help="Enter your email address")
        self.parser.add_argument("-r","--receivers", required=True,
                                 help="Enter receiver email addresses ")
        self.parser.add_argument("-t","--subject", required=True, help="Enter the subject")
        self.parser.add_argument("-b","--body", required=True, help="Enter the body of your email")

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
