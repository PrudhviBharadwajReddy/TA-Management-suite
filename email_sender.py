import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Replace the below details with your own
sender_email = "tamanagementsuite@gmail.com" # TA app official email
app_password = "jwvctuybkduuvnic" # app password (without spaces)


def send_email(receiver_email, subject, body):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add body to the email
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Create SMTP session for sending the mail
        server = smtplib.SMTP('smtp.gmail.com', 587) # Use 465 for SSL
        server.starttls() # Enable security
        server.login(sender_email, app_password) # Login with your Gmail and app password
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")



#receiver_email = "chiru.namani4444@gmail.com" # Receiver's email
#subject = "Application Successfully Submitted - TA Management Suite"


body = """
We are pleased to inform you that your application has been successfully submitted to the TA Management Suite. This email serves as a confirmation of your submission.

Application Details:
--------------------
Application ID: 8723873\n
Submitted On: 12/06/2023\n
\n
What's Next?\n
------------\n
Your application will now be reviewed by TA team. The review process typically takes couple of days. During this period, we may contact you if additional information is needed.\n
\n
Stay Updated:\n
-------------\n
You can check the status of your application at any time by logging into your account on the TA Management Suite portal.\n
\n
Need Assistance?\n
----------------\n
If you have any questions or need further assistance, feel free to reach out to us at [Support Contact Information].\n
\n
Thank you for choosing TA Management Suite for your teaching assistantship management needs. We look forward to the possibility of working with you.\n
\n
Best regards,\n

[Your Name or Team's Name]
TA Management Suite Team
[Contact Information or Website]

Note: This is an automated message. Please do not reply directly to this email.
"""

# Send the email
#send_email(sender_email, app_password, receiver_email, subject, body)
