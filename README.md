# Python Email Automation Project

A command-line interface tool for sending and receiving emails securely and efficiently using Python. Includes support for email scanning, CLI flags, and cross-platform script shortcuts.

---

## Features 🚀

1. ✅ Send and receive emails via command line  
2. 💾 Custom email filtering (future enhancement)  
3. 🔡 Attachment safety scan (new!)  
   - Scans attachments before download using the VirusTotal API  
   - Prompts user based on the scan result  
   - Helps avoid downloading malicious files  
4. 🖥️ Windows Command Interface Support  
   - Run CLI scripts globally from CMD or PowerShell  
   - `.bat` scripts added in `script/` folder  
   - Works via terminal shortcut using Python’s `-m` module support  
5. 🔐 Optional: OAuth authentication (planned)  
6. 🔍 Enhanced security checks for malicious attachments and phishing emails  
   - Detects suspicious links and common phishing patterns  
   - Warns users before opening or downloading risky content  
7. 📅 Schedule emails for future delivery  
   - Set specific dates and times to send emails automatically  

---

## Requirements 📌

**System Requirements**
- Python **3.6 or higher**
- An active SMTP-enabled email account (e.g., Gmail, Outlook, Yahoo)

**Required Python Libraries**  
Install the required dependencies using pip:

```bash
pip install smtplib imaplib argparse getpass email
```

---

## Installation & Setup ⚙️

1. **Clone this repository:**
   ```bash
   git clone https://github.com/coding-enthusiast003/python-email-projects.git
   cd python-email-projects
   ```
   2. **Sending Emails**
      ```bash
      python -m send_mails.send3 -u "youremail@gmail.com" -r "recipient@example.com" -t "Subject" -b "Message Body"
      ```
      > **Note:**  
      > In the `send3` module, you can either provide all arguments via the command line, or just specify your email address (`-u`). If you omit other options, the script will interactively prompt you for the remaining details (recipient, subject, body, etc.).
      Enter your email password securely when prompted.

   3. **Receiving Emails**
      ```bash
      python -m received_mails.receiver2 -s "example@gmail.com"
      ```
      Securely prompted for entering password

---

## 🪟 Setting Up Email CLI Shortcuts on Windows

You can run the email sender and receiver from any terminal (CMD or PowerShell) using simple commands.

### 📁 Step 1: Create Two Batch Files

Create a folder for your scripts (e.g., `D:\scripts`) and inside that folder, create two `.bat` files:

#### 1️⃣ `email-send.bat`

```bat
@echo off
REM Change this path to the root of your project directory
cd /d "D:\email-project"
python -m send_mails.send2 %*
```

#### 2️⃣ `email-receive.bat`

```bat
@echo off
REM Change this path to the root of your project directory
cd /d "D:\email-project"
python -m received_mails.receiver2 %*
```

### ⚙️ Step 2: Add to System PATH

1. Press `Win + S`, search for **Environment Variables**, and open it  
2. Click **Environment Variables**  
3. Under **System variables**, select `Path` → click **Edit**  
4. Click **New** → paste the path where your `.bat` files are located (e.g., `D:\scripts\`)  
5. Click **OK** to apply the changes  

---

### ✅ Step 3: Run Anywhere

Now you can simply open **Command Prompt** or **PowerShell** and type:

```bash
email-send -s "your_email@gmail.com"
email-receive -u "your_email@gmail.com"
```

---

## Security Best Practices 🔐

- **DO NOT** hardcode email credentials inside the script.
- Use **environment variables** or a configuration file.
- Consider **OAuth authentication** for better security.

---

## Future Enhancements 🚀


- 📢 Bulk email sending with rate limits
- 🛡️ Implementing OAuth authentication for enhanced security

---

## Contributing 🤝

Feel free to fork this repository and submit pull requests with improvements!

## License 📜

This project is licensed under the **MIT License**.

---

Made with ❤️ by [Subham Das (coding-enthusiast003)]

