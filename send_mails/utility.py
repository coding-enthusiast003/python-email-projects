from pyfiglet import Figlet # For creating ASCII art text
from rich.console import Console # For rich console output
from rich.text import Text # For rich text formatting

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
    console.print("[bold green]Your one-stop solution for sending and receiving emails with ease![/bold green]")