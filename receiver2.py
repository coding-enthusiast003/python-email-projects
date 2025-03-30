from receiver1 import EmailReceiver , CommandInterface


class Interface(EmailReceiver,CommandInterface):
    def __init__(self):
        super().__init__()
        self.fetch_mails()  # Fetch emails when the interface is initialized