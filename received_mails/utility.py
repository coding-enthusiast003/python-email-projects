from bs4 import BeautifulSoup  # For parsing HTML content
import webbrowser  # To open URLs in the default browser
from rich.console import Console  # For rich console output
import os  # To handle file operations
from pyfiglet import Figlet
from rich.console import Console
from rich.text import Text

console = Console()

def extract_text_from_html(html_content: str) -> str:
    """
    Extracts plain text from HTML content.

    Args:
        html_content (str): The HTML content to parse.

    Returns:
        str: Extracted plain text.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(strip=True)



def open_url(message_id: str) -> None:
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



def save(filename: str, content: bytes) -> None:
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


def ui():
    """
    Displays a colorful UI using Rich and PyFiglet.
    """
    # Create a console instance
    console = Console()

    # Create a Figlet instance with a specific font
    fig = Figlet(font='slant')  # Try 'standard', 'slant', 'big', etc.

    # Create colored segments
    py_text = Text(fig.renderText("Pigeon"), style="bold green")
    term_text = Text(fig.renderText("Mail"), style="bold blue")
     
    # Print them together
    console.print(py_text)
    console.print(term_text)
    

    console.print("\n" + "-" * 50)  # Divider line