from bs4 import BeautifulSoup
import webbrowser  # Importing webbrowser to open URLs in the default browser
from rich.console import Console

console = Console()

def extract_text_from_html(html_content):  # Function to extract text from HTML CONTENT
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(strip=True)


def open_url(message_id):
    
        # Add option to open the email in Gmail
        if message_id:
            open_in_browser = console.input("[bold green]Do you want to open this email in Gmail? (y/n): [/bold green]").strip().lower()
            if open_in_browser == 'y':
                gmail_url = f"https://mail.google.com/mail/u/0/#search/rfc822msgid:{message_id}"
                webbrowser.open(gmail_url)
                console.print(f"🌐 Opened email in browser: {gmail_url}", style="cyan")
