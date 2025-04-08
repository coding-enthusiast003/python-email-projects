# Python Email Automation Project

Automate email sending and receiving tasks in Python using the **SMTP protocol** and **IMAPLIB protocol** via a user-friendly **command-line interface (CLI)**.

## Features 🚀

## ✉️ Sending Emails
- 📩 Send emails using an SMTP server (Gmail, Outlook, Yahoo, etc.).
- 🔒 Securely prompt for the sender's email password (no hardcoded credentials).
- 📜 Support for multiple recipients.
- 📎 Attach files (PDF, images, audio, etc.).
- ⚡ Command-line interface for easy configuration.
- ✅ Supports both **TLS & SSL encryption**.
- 📝 Send plain text or **HTML-formatted** emails.

### 📥 Receiving Emails
- 📬 Fetch emails using IMAP protocol
- 📂 List and read recent emails with proper formatting.
- 🧾 Display email details like **sender, subject, and body**.
- 📎 List and download attachments directly to your system
- 🧠 Handles multipart emails and **inline attachments** smartly.

## Requirements 📌
Ensure you have the following before running the project:

### **System Requirements**
- Python **3.6 or higher**
- An active SMTP-enabled email account (e.g., Gmail, Outlook, Yahoo)

### **Required Python Libraries**
Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```
Or install them manually:
```bash
pip install smtplib imaplib argparse getpass email
```

## Installation & Setup ⚙️
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/python-email-projects.git
   cd python-email-projects
   ```

2. **Sending Emails**

   Run the script with required arguments:
   ```bash
   python send_email/main2.py \
      --sender example@gmail.com \
      --receiver test@gmail.com \
      --subject "Test Email" \
      --body "Hello, this is a test email!" \
      --files "file1.pdf" "file2.jpg"
   ```

3. Enter your email password securely when prompted.

4. **Receiving Emails**

   To receive and read emails from your inbox:
   ```bash
   python receive_mail/receiver2.py \
      --email "example@gmail.com" \
       
   ```

## Security Best Practices 🔐
- **DO NOT** hardcode email credentials inside the script.
- Use **environment variables** or a configuration file.
- Consider **OAuth authentication** for better security.

## Future Enhancements 🚀
 
- 🔍 **Checking for malicious attachments or phishing emails**
- 📅 **Scheduling emails for future sending**
- 📢 **Bulk email sending with rate limits**
- 🛡️ **Implementing OAuth authentication for enhanced security**

## Contributing 🤝
Feel free to fork this repository and submit pull requests with improvements!

## License 📜
This project is licensed under the **MIT License**.

---
Made with ❤️ by [Rishi(coding-enthusiast003)]

