# emailer.py
import smtplib
from email.message import EmailMessage
from datetime import datetime

def send_alert_email(target_ip, failure_count, email_settings, recipients):
    """Connects to Office 365 SMTP server and sends an alert email."""
    if not all([email_settings, email_settings['sender_email'], email_settings['sender_password'], recipients]):
        print("Email settings or recipients not configured. Skipping email alert.")
        return

    print(f"Attempting to send email alert for {target_ip}...")

    msg = EmailMessage()
    msg['Subject'] = f"Network Alert: Host {target_ip} is Unreachable"
    msg['From'] = email_settings['sender_email']
    # The 'To' field needs a comma-separated string of emails
    msg['To'] = ", ".join([r['email'] for r in recipients])
    msg.set_content(
        f"This is an automated alert from the Network Monitor application.\n\n"
        f"The host {target_ip} has been unreachable for {failure_count} consecutive checks.\n\n"
        f"Timestamp of alert: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(email_settings['sender_email'], email_settings['sender_password'])
            server.send_message(msg)
        print("Email alert sent successfully.")
    except Exception as e:
        print(f"Email alert failed: An unexpected error occurred: {e}")