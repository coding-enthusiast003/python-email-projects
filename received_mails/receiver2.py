import os
import email
from received_mails.text_extract import extract_text_from_html  # Importing the function from text_extract.py
import getpass
import textwrap
import shutil
from received_mails.receiver1 import CommandInterface
from received_mails.scanfile import scan_attachment  # Importing specific function from scanfile.py
import webbrowser  # Import webbrowser module to open HTML files

# Get terminal width, fallback to 100
terminal_width = shutil.get_terminal_size((100, 20)).columns
wrap_width = terminal_width - 4  # Small margin for clean look
 
def extract_body(msg):
    """
    Extracts the plain text body, HTML content, and attachments from an email message.
    """
    body = ""
    html_content = None
    attachments = []

    try:
        # Check if the email has multiple parts (e.g., text + attachments)
        if msg.is_multipart():
            for part in msg.walk():  # walk() in email module is used to iterate through the parts of the email message.
                # Get the content type and disposition (header that indicates if the part is an attachment)
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                # Extract the plain text content
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        decoded_payload = part.get_payload(decode=True)
                        body = decoded_payload.decode() if decoded_payload else "(Empty Body)"
                    except Exception:
                        body = "Failed to decode email body."

                # Extract HTML content and convert it to plain text
                elif content_type == "text/html" and "attachment" not in content_disposition:
                    try:
                        html_payload = part.get_payload(decode=True)
                        if html_payload:
                            html_content = html_payload.decode()  # Decode the HTML content
                            body = extract_text_from_html(html_content)  # Convert HTML to plain text
                        else:
                            html_content = None
                    except Exception:
                        html_content = None
                        body = "Failed to decode HTML content."

                # Collect attachment filenames and content
                elif "attachment" in content_disposition:
                    filename = part.get_filename()
                    content = part.get_payload(decode=True)
                    if filename and content:
                        attachments.append((filename, content))

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
         
    
    return body, html_content, attachments

 
class CommandInterface2(CommandInterface): #Inherited class from CommandInterface class
    """
    Command-line interface for fetching and displaying email details, including attachments.
    """
    def __init__(self):
        super().__init__()
        self.api_key = None  # API key for VirusTotal

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
                    body, html_content, attachments = extract_body(msg)

                    # Display the email content inside a formatted box
                    print("-" * 100)  # Top divider

                    print(f"Email ID: {mail_id}")
                    print(f"From: {msg['From']}")
                    print()

                    print("Body:")
                    print()  # Empty line for spacing

                    for line in textwrap.wrap(body, width=wrap_width):  #   Wrap the body text(to fit the terminal width)
                        print(f"{line}")

                    print()

                    # Handle HTML content
                    if html_content:
                        save_html = input("This email contains HTML content. Do you want to save and view it? (y/n): ").strip().lower()
                        if save_html == 'y':
                            html_file = f"email_{mail_id}.html"
                            with open(html_file, "w", encoding="utf-8") as f:
                                f.write(html_content)
                            print(f"✅ HTML content saved as {html_file}")
                            open_html = input("Do you want to open the HTML content in your browser? (y/n): ").strip().lower()
                            if open_html == 'y':
                                webbrowser.open(html_file)
                        print()

                    
                    print("Attachments:")
                    if attachments:
                        
                        for filename, content in attachments:
                            size_kb = len(content) / 1024  # Calculate size in KB
                            for line in textwrap.wrap(f"🔗 {filename} ({size_kb:.2f} KB)", width=wrap_width):
                                print(line) # Display attachments with memory details

                            print() #printing empty line for spacing
                            print()
                            # Scan the attachment using VirusTotal API for safety
                            prompt = input(f"Do you want to scan the attachment '{filename}' for safety? (y/n): ").strip().lower()
                            if prompt == 'y' :
                                self.api_key = input("Please enter your VirusTotal API key: ").strip()
                                print("scanning attachments, please wait ...")
                                print("It may take a few seconds to complete...")
                                if scan_attachment(content, filename, self.api_key):
                                    print()
                                    print("✅ Attachment is safe.")
                                else:
                                    print("⚠️ Attachment flagged as unsafe.")
                            print()
                            print()

                            # Prompt to save the attachment
                            save_attachments = input("Do you want to save the attachments? (y/n): ").strip().lower()
                            if save_attachments == 'y':
                                # Save the attachment to the current working directory

                                file_path = os.path.join(os.getcwd(), filename)
                                with open(file_path, "wb") as f:
                                    f.write(content)
                                    print(f"✅ Saved attachment: {filename} to {file_path}")
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
