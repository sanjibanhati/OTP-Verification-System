import gradio as gr
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import getpass
import os

# Global variable to store OTP
otp = None
email = None


def generate_otp():
    return random.randint(100000, 999999)

def validate_email(email):
    # Simple regex for basic email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

#sender_email = os.getenv('sender_email')
#sender_password = os.getenv('sender_password')

def send_otp_via_email(receiver_email, otp):
    # Sender email configuration
    sender_email = "Sanjiban.Hati@gmail.com"  # Replace with your email
    sender_password = "eyml lznl jpoc irod"
    subject = "Your OTP Code"
    body = f"Your OTP code is {otp}. Please enter this code to verify your email."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Check if the email is valid
        if not validate_email(receiver_email):
            return "Invalid email address format. Please check the email and try again."
        
        # Attempt to send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return "OTP sent successfully."
    
    except smtplib.SMTPRecipientsRefused:
        return "Failed to send OTP. The recipient's email address is invalid."
    except smtplib.SMTPAuthenticationError:
        return "Failed to send OTP. Authentication failed. Check your email credentials."
    except smtplib.SMTPException as e:
        return f"Failed to send OTP. SMTP error: {e}"
    except Exception as e:
        return f"Failed to send OTP. Error: {e}"

def verify_otp(user_otp):
    global otp
    if otp is None:
        return "No OTP generated."
    if user_otp.isdigit() and len(user_otp) == 6:
        if int(user_otp) == otp:
            return "OTP verified successfully. Access granted."
        else:
            return "Incorrect OTP. Access denied."
    else:
        return "Invalid OTP format. Please enter a 6-digit OTP."

def gradio_interface(email_input, otp_input):
    global otp, email
    if email_input and otp_input == "":
        email = email_input
        otp = generate_otp()
        return send_otp_via_email(email, otp)
    elif otp_input:
        return verify_otp(otp_input)
    else:
        return "Please provide your email address or OTP."

# Define Gradio interface
interface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Textbox(label="Enter your email address", placeholder="user@example.com", lines=1),
        gr.Textbox(label="Enter OTP received", placeholder="******", lines=1, type="password")
    ],
    outputs="text",
    live=True
)

# Launch the interface
interface.launch()
