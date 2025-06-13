import email
from received_mails.utility import *  # Importing the function from utility.py
import textwrap
import shutil
from received_mails.receiver1 import CommandInterface
from received_mails.scanfile import scan_attachment  # Importing specific function from scanfile.py
from rich.console import Console


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
                content_disposition = str(part.get("Content-Disposition") or "")
                filename = part.get_filename()

                # Extract the plain text content
                if content_type == "text/plain" and "attachment" not in content_disposition and not body:
                    try:
                        decoded_payload = part.get_payload(decode=True)
                        body = decoded_payload.decode() if decoded_payload else "(Empty Body)"
                    except Exception:
                        body = "Failed to decode email body."

                # Extract HTML content and convert it to plain text
                if content_type == "text/html" and "attachment" not in content_disposition and not html_content:
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

                # Collect any part with a filename as an attachment (covers inline images/videos)
                if filename:
                    content = part.get_payload(decode=True)
                    if content:
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
         
    
    return body, html_content, attachments, msg.get("Message-ID")  # Explicitly calling msg.get("Message-ID")

 
class CommandInterface2(CommandInterface): #Inherited class from CommandInterface class
    """
    Command-line interface for fetching and displaying email details, including attachments.
    """
    def __init__(self):
        super().__init__()
        self.api_key = None  # API key for VirusTotal
        self.console = Console() # Console instance for rich text display
        self.connection = None  # Connection instance

    def final_run(self):
        """
        Overrides the final_run method to include file attachments.
        Fetch and display email details along with attachments.
        """
        try:
            # Parse command-line arguments
            args = self.parser.parse_args()
           
            # Prompt for password securely if not provided as an argument
            self.password = args.password if args.password else self.console.input("[bold green]Please enter your email password (input will be hidden):[/bold green] ", password=True)

            # Set user details (username and password)
            self.user_details(username=args.username, password=self.password)

            # Establish connection to the email server
            if self.connection is None:
                try:
                    self.connection = self.server_setup()  # Establish connection once
                    if self.connection:
                         # Call the UI function only after a successful connection
                        ui()  # Display the UI after successful connection
                        
                        self.fetch_mails() # Fetch emails after connection
                    else:
                        raise ConnectionError("Failed to establish connection.")
                   
                except Exception as e:
                    raise ConnectionError(f"Connection Error: {e}")
                    
            

            while True:
                # Prompt user for an email ID to fetch
                mail_id = self.console.input("[bold green]Enter the email ID to fetch content (or 'q' to quit):[/bold green] ").strip()

                if mail_id.lower() == 'q': #Quit the process
                    self.console.print("Exiting...", style="bold cyan")
                    break

                status, msg_data = self.connection.fetch(mail_id, "(RFC822)")

                if status == 'OK' and msg_data[0] is not None:
                    raw_email = msg_data[0][1]
                    if isinstance(raw_email, bytes): # Check if raw_email is in bytes format
                        msg = email.message_from_bytes(raw_email) # Create email message from bytes
                        body, html_content, attachments, message_id = extract_body(msg)  # Assigning message_id
                    else:
                        print("❌ Failed to fetch email content: Data is not in bytes format.")
                        continue

                    # Display the email content inside a formatted box
                    print("-" * 100)  # Top divider

                    print(f"Email ID: {mail_id}")
                    print(f"From: {msg['From']}")
                    print()

                    print("Body:")
                    print()  # Empty line for spacing

                    for line in textwrap.wrap(body, width=wrap_width):  #   Wrap the body text(to fit the terminal width)
                        self.console.print(f"[bold white on black]{line}[/bold white on black]")

                    print()
                    save_html_choice = self.console.input("[bold green]Do you want to save the HTML content? (y/n): [/bold green]").strip().lower()
                    if save_html_choice == "y" and html_content:
                        # Save the HTML content to a file
                        filename = f"email_{mail_id}.html"
                        save_html(filename , html_content)  # Using the save_html function from utility.py
                    else:
                        self.console.print("HTML content unable to save or not provided.", style = "yellow")

                    self.console.print("[cyan]Attachments:[/cyan]")
                    if attachments:
                        
                        for filename, content in attachments:
                            size_kb = len(content) / 1024  # Calculate size in KB
                            for line in textwrap.wrap(f"🔗 {filename} ({size_kb:.2f} KB)", width=wrap_width):
                                self.console.print(f"[bold white underline]{line}[/bold white underline]") # Display attachments with memory details

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
                                    self.console.print("✅ Attachment is safe.", style="green")
                                else:
                                    self.console.print("⚠️ Attachment flagged as unsafe.", style="bold red")
                            print()
                            print()

                                # Prompt to save the attachment
                            save_attachments = self.console.input("[bold green]Do you want to save the attachments? (y/n): [/bold green]").strip().lower()
                            if save_attachments == 'y':
                                # Save the attachment to the current working directory
                                filename = filename.replace("/", "_")  # Replace any slashes in the filename to avoid directory issues
                                save(filename, content)  # Using the save function from utility.py

                            print()
                            
                    else:
                        self.console.print("Attachment : None", style="yellow")
                    if message_id:
                        #calling the function from utility.py to open the email in browser
                        open_url(message_id)  # Using message_id to open in gmail 
                    else:
                        self.console.print("⚠️ No Message-ID found for this email.", style="yellow")

                    self.console.print("-" * 100, style="bold white")  # Bottom divider


                else:
                    print(f"❌ Email with ID {mail_id} not found.")

            self.connection.logout() #Log out from the Email server after processing

        except KeyboardInterrupt:
            self.console.print("[bold red]Program interrupted by user.[/bold red]")
        except SystemExit:
            self.console.print("[bold red]Program exited.[/bold red]")    
        except Exception as e:
            print(f"An error occurred: {e}")
        
        
if __name__== "__main__":
    prompt = CommandInterface2()
    prompt.final_run()
