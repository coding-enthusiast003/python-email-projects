from pyfiglet import Figlet # For creating ASCII art text
from rich.console import Console # For rich console output
from rich.text import Text # For rich text formatting
import time
from datetime import datetime , timedelta # For handling date and time operations
 
# Create a console instance
console = Console()


def ui():
    """
    Displays a colorful UI using Rich and PyFiglet.
    """

    # Create a Figlet instance with a specific font
    fig = Figlet(font='slant')  # Try 'standard', 'slant', 'big', etc.

    # Create colored segments
    py_text = Text(fig.renderText("Pigeon Mail"), style="bold cyan")
     # Print them together
    console.print(py_text)

    console.print("[bold blue]Welcome to Pigeon Mail![/bold blue]")

    console.print("\n" + "-" * 50)  # Divider line
    console.print("[bold green]Your one-stop solution for sending and receiving emails with ease![/bold green]")


def time_scheduler(input_time, msg, server_connection):
    '''
    Automatically schedules the email to be sent at a scheduled time.
    '''
    # Placeholder for time scheduling logic
    now = datetime.now()

    try:
        input_hour, input_minute = map(int, input_time.split(":"))  #MAP FUNCTION TO CONVERT INPUT TO INTEGER AND SPLIT IT INTO HOUR AND MINUTE
    except ValueError:
        console.print("[bold red]Invalid time format. Please enter a valid time in HH:MM format.[/bold red]")
        return
    
    # Check if the input time is valid
    if not (0 <= input_hour < 24 and 0 <= input_minute < 60):
        console.print("[bold red]Invalid time format. Please enter a valid time in HH:MM format.[/bold red]")
        return

    scheduled_time = now.replace(hour=input_hour, minute=input_minute, second=0, microsecond=0) # replace the current time with the scheduled time
    if scheduled_time < now:
        scheduled_time += timedelta(days=1) # If the scheduled time is in the past, schedule it for the next day
        # timedelta method is used to add a day to the scheduled time
        console.print("[bold yellow]Scheduled time is in the past. Rescheduling to the next day.[/bold yellow]")

    print()
    console.print(f"Email will be sent at {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}", style= "bold green")
    print()
    print()
    wait_time = (scheduled_time - now).total_seconds() # Calculate the wait time in seconds
    time.sleep(wait_time)
    server_connection(msg)  # Send the email after waiting