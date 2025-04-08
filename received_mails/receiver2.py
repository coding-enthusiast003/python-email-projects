import imaplib
import email
from email.header import decode_header
import getpass
import textwrap
import shutil
from receiver1 import  CommandInterface

# Get terminal width, fallback to 100
terminal_width = shutil.get_terminal_size((100, 20)).columns
wrap_width = terminal_width - 4  # Small margin for clean look
 
def extract_body(msg):
    """
    Extracts the plain text body and attachments from an email message.
    """
 
    body = ""
    attachments = []

    try:
        # Check if the email has multiple parts (e.g., text + attachments)
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))  
                
                # Extract the plain text content
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        decoded_payload = part.get_payload(decode=True)
                        body = part.get_payload(decode=True).decode() if decoded_payload else "(Empty Body)"
                    except Exception:
                        body = "Failed to decode email body."

                # Collect attachment filenames
                elif "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append(filename)

        else:
            # If the email is not multipart, extract body directly
            try:
                decoded_payload = msg.get_payload(decode=True)
                body = decoded_payload.decode() if decoded_payload else "(Empty Body)"
            except Exception as e:
                print(f"❌ Failed to decode email body: {e}")
                body = "Failed to decode email body."

    except Exception as e:
        print(f"❌ Error processing email parts: {e}")
         
    
    return body, attachments

 
class CommandInterface2(CommandInterface): #Inherited class from CommandInterface class
    """
    Command-line interface for fetching and displaying email details, including attachments.
    """
    def __init__(self):
        super().__init__()

    def final_run(self):
        """
        Overrides the final_run method to include file attachments.
        Fetch and display email details along with attachments.
        """
        try:
            # Parse command-line arguments
            args = self.parser.parse_args()

            # Prompt for password securely if not provided as an argument
            self.password = args.password if args.password else getpass.getpass("Please enter your email password (input will be hidden): ")

            # Set user details (username and password)
            self.user_details(username=args.username, password=self.password)

            # Fetch a list of available emails             
            self.fetch_mails()

            connection1 = self.server_setup()  # Establish connection to the email server

            while True:
                # Prompt user for an email ID to fetch
                mail_id = input("Enter the email ID you want to fetch (or 'q' to quit): ")

                if mail_id.lower() == 'q': #Quit the process
                    print("Exiting...")
                    break

                status, msg_data = connection1.fetch(mail_id, "(RFC822)")

                if status == 'OK' and msg_data[0] is not None:
                    msg = email.message_from_bytes(msg_data[0][1])
                    body, attachments = extract_body(msg)

                    # Display the email content inside a formatted box
                    print("-" * 100)  # Top divider

                    print(f"Email ID: {mail_id}")
                    print(f"From: {msg['From']}")
                    print()

                    print("Body:")
                    print()  # Empty line for spacing

                    for line in textwrap.wrap(body, width=wrap_width):  # Slightly under 100 to avoid full-width wrapping issues
                        print(f"{line}")

                    print()

                    # Display attachments
                    print("Attachments:")
                    if attachments:
                        for file in attachments:
                            for line in textwrap.wrap(f"🔗 {file}", width=wrap_width):
                                print(line)
                    else:
                        print("Attachment : None")

                    print("-" * 100)  # Bottom divider


                else:
                    print(f"❌ Email with ID {mail_id} not found.")

            connection1.logout() #Log out from the Email server after processing
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__== "__main__":
    prompt = CommandInterface2()
    prompt.final_run()
