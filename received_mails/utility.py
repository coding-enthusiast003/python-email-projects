from bs4 import BeautifulSoup  # For parsing HTML content
import webbrowser  # To open URLs in the default browser
from rich.console import Console  # For rich console output
import os  # To handle file operations
from pyfiglet import Figlet # For creating ASCII art text
from rich.text import Text # For rich text formatting

console = Console()

def extract_text_from_html(html_content: str) -> str: #function to extract text from HTML content
    """
    Extracts plain text from HTML content.

    Args:
        html_content (str): The HTML content to parse.

    Returns:
        str: Extracted plain text.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(strip=True)



def open_url(message_id: str) -> None: #function to open the email in gmail
    """
    Opens an email in Gmail using its message ID.

    Args:
        message_id (str): The unique message ID of the email.
    """
    if message_id:
        open_in_browser = console.input(
            "[bold green]Do you want to open this email in Gmail? (y/n): [/bold green]"
        ).strip().lower()
        if open_in_browser == 'y':
            gmail_url = f"https://mail.google.com/mail/u/0/#search/rfc822msgid:{message_id}"
            webbrowser.open(gmail_url)
            console.print(f"🌐 Opened email in browser: {gmail_url}", style="cyan")


def save(filename: str, content: bytes) -> None: #function to save the attachment
    """
    Saves content to a file.

    Args:
        filename (str): The name of the file to save.
        content (bytes): The binary content to write to the file.
    """
    try:
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, "wb") as f:
            f.write(content)
        console.print(f"✅ Saved attachment: {filename} to {file_path}", style="green")
    except Exception as e:
        console.print(f"❌ Failed to save attachment: {filename}. Error: {e}", style="red")


def save_html(filename: str, content: str) -> None: #function to save the html content of an email to a file
    """
    Saves HTML content to a file.

    Args:
        filename (str): The name of the file to save.
        content (str): The HTML content to write to the file.
    """
    try:
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        console.print(f"✅ Saved HTML content: {filename} to {file_path}", style="green")
    except Exception as e:
        console.print(f"❌ Failed to save HTML content: {filename}. Error: {e}", style="red")


def ui():
    """
    Displays a colorful UI using Rich and PyFiglet.
    """
    # Create a console instance
    console = Console()

    # Create a Figlet instance with a specific font
    fig = Figlet(font='slant')  # Try 'standard', 'slant', 'big', etc.

    # Create colored segments
    py_text = Text(fig.renderText("Pigeon Mail"), style="bold cyan")
     # Print them together
    console.print(py_text)
    

    console.print("[bold blue]Welcome to Pigeon Mail![/bold blue]")
    
    console.print("\n" + "-" * 50)  # Divider line
    
    
     
def delete(mail_id: str, connection) :
    """
    Deletes an email by its ID.

    Args:
        mail_id (str): The unique ID of the email to delete.
    """
    try:
        ask = input("Do you want to delete this email? (y/n): ").strip().lower()
        if ask != 'y':
            return  # Exit if the user does not want to delete the email
        
        # Mark the email for deletion
        status, response = connection.uid('STORE', mail_id, '+FLAGS', '(\\Deleted)')
        if status == 'OK':
            console.print(f"✅ Email with ID {mail_id} marked for deletion.", style="green")
            
            # Expunge to permanently delete the email
            connection.expunge()
            console.print(f"✅ Email with ID {mail_id} permanently deleted.", style="green")
        else:
            console.print(f"❌ Failed to delete email with ID {mail_id}.", style="red")
        
        
    except Exception as e:
        console.print(f"❌ An error occurred while deleting email: {e}", style="red")





