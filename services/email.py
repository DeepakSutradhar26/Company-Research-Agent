import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

def send_email(to: str, name: str, company: str, pdf_path: str):
    try:
        sender = os.getenv('EMAIL')
        password = os.getenv('EMAIL_PASSWORD')

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = to
        msg['Subject'] = f'Your Company Intelligence Report - {company}'

        body = f"""Hi {name},

Thank you for your interest in SimplifIQ.

Please find attached your personalized intelligence report for {company}.

Best regards,
SimplifIQ Team"""

        msg.attach(MIMEText(body, 'plain'))

        # Attach PDF
        with open(pdf_path, 'rb') as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_path)}')
            msg.attach(attachment)

        # Send
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, to, msg.as_string())

        return {'success': True}

    except Exception as e:
        return {'success': False, 'message': str(e)}