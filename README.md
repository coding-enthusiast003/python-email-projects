# Python Email Automation Project

A command-line interface tool for sending and receiving emails securely and efficiently using Python. Includes support for email scanning, CLI flags, and cross-platform script shortcuts.



## Features 🚀
1. ✅ Send and receive emails via command line

2. 💾 Custom email filtering (future enhancement)

3. 🔡️ Attachment safety scan (new!)

   - Scans attachments before download using the VirusTotal API

   - Prompts user based on the scan result

   - Helps avoid downloading malicious files

4. 🖥️ Windows Command Interface Support

   - Run CLI scripts globally from CMD or PowerShell

   - .bat scripts added in script/ folder

   - Works via terminal shortcut using Python’s -m module support

5. 🔐 Optional: OAuth authentication (planned)



## Requirements 📌
Ensure you have the following before running the project:

### **System Requirements**
- Python **3.6 or higher**
- An active SMTP-enabled email account (e.g., Gmail, Outlook, Yahoo)

### **Required Python Libraries**
Install the required dependencies using pip:

install them manually:
```bash
pip install smtplib imaplib argparse getpass email
```

## Installation & Setup ⚙️
1. Clone this repository:
   ```bash
   git clone https://github.com/coding-enthusiast003/python-email-projects.git
   cd python-email-projects
   ```

2. **Sending Emails**

   Run the script with required arguments:
   ```bash
   sendmail -u "youremail@gmail.com" -to "recipient@example.com" -s "Subject" -b "Message Body"
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

