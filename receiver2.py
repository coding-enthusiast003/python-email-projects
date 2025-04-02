import imaplib
import email
from email.header import decode_header
import getpass
import argparse
from receiver1 import EmailReceiver, CommandInterface

def extract_body(msg):
 
    body = ""
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))  

            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    decoded_payload = part.get_payload(decode=True)
                    body = part.get_payload(decode=True).decode() if decoded_payload else "(Empty Body)"
                except Exception:
                    body = "Failed to decode email body."
            elif "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    attachments.append(filename)

    else:
        try:
           decoded_payload = msg.get_payload(decode=True)
           body = decoded_payload.decode() if decoded_payload else "(Empty Body)"
        except Exception as e:
            print(f"❌ Failed to decode email body: {e}")
            body = "Failed to decode email body."

        print("\n📝 **Email Body:**\n" + ("-" * 50))
        print(body)
        print("-" * 50)

    if attachments:
        print("\n📎 **Attachments Found:**")
        for file in attachments:
                print(f"🔗 {file}")
    return body, attachments

 
class CommandInterface2(CommandInterface):
    def __init__(self):
        super().__init__()

    def final_run(self):
        """
        Overrides the final_run method to include file attachments.
        """
        try:
            args = self.parser.parse_args()

            self.password = args.password if args.password else getpass.getpass("Please enter your email password (input will be hidden): ")

            self.user_details(username=args.username, password=self.password)

             
            self.fetch_mails()

            connection1 = self.server_setup()

            while True:
                mail_id = input("Enter the email ID you want to fetch (or 'q' to quit): ")

                if mail_id.lower() == 'q':
                    print("Exiting...")
                    break

                status, msg_data = connection1.fetch(mail_id, "(RFC822)")

                if status == 'OK' and msg_data[0] is not None:
                    msg = email.message_from_bytes(msg_data[0][1])
                    body, attachments = extract_body(msg)
                    print(f"\n📝 Extracted Email Body:\n{body}")  # Debugging print
                else:
                    print(f"❌ Email with ID {mail_id} not found.")

            connection1.logout()
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__== "__main__":
    prompt = CommandInterface2()
    prompt.final_run()
