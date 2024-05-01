import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Function to load the student database from a file
def load_database():
    try:
        with open("student_database.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

# Function to check default_mask and send email if exceeds 10
def check_and_send_email():
    student_database = load_database()
    current_month = datetime.now().strftime("%B")
    emails_sent = False

    for student_id, student_info in student_database.items():
        default_mask_count = student_info.get("default_mask", 0)
        if default_mask_count > 10:
            student_name = student_info.get("name", "Unknown")
            student_email = student_info.get("email", "")
            message = f"Dear {student_name},\n\nYour default_mask count has exceeded 10 for the month of {current_month}. Please pay the fine of RS.579 to abcd@okaybank UPI ID if you would like to give the upcoming semester exam.\n\nRegards,\nUtkal University"
            send_email(student_email, "Notification: Default Mask Exceeds Limit", message)
            print(f"Email sent successfully to {student_email} for {student_name}")
            emails_sent = True

    if not emails_sent:
        print("No emails were sent because all default_mask counts are within the limit.")

# Function to send email
def send_email(receiver_email, subject, message):
    try:
        sender_email = "projectworks12345@outlook.com"  # Your Outlook email address
        sender_password = "Projectworks@12345"  # Your Outlook email password

        # Create a MIMEText object
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        # Establish a connection with the SMTP server
        server = smtplib.SMTP("smtp.office365.com", 587)  # Outlook SMTP server and port
        server.starttls()

        # Login to the email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Close the connection
        server.quit()

        print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print(f"An error occurred while sending email to {receiver_email}: {e}")

# Main function to check and send emails
def main():
    check_and_send_email()

if __name__ == "__main__":
    main()
