#we are using here regex(regular-expression module) which is generally used in pattern checking

import re

def emailcheck():
    email= input("enter your email :")
    email_pattern = r"^(?!.*[._%+-]{2})[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$"

    # Check if the email matches the pattern, with case insensitivity
    if re.match(email_pattern, email,re.IGNORECASE):
        print("Valid email")
    else:
        print("Invalid email..please try again")
    return email

check= emailcheck()
print(check)