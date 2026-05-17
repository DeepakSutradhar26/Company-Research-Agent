import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

def send_email(to: str, name: str, company: str, pdf_path: str):
    sender = os.getenv('EMAIL')
    password = os.getenv('EMAIL_PASSWORD')

    try:
        msg = MIMEMultipart()
        body = MIMEText(f"""Hi {name},

        This is your requested company intelligence report for {company}.

        The detailed analysis is attached as a PDF file.

        It includes:
        - Company overview
        - Key insights
        - Web and public data summary
        - AI-generated analysis report

        Please review the attachment for full details.

        Regards,
        Company-Research-Agent
        """)
        msg.attach(body)
        msg['From'] = sender
        msg['To'] = to
        msg['Subject'] = f'Your Company Intelligence Report - {company}'

        # Attach PDF
        with open(pdf_path, "rb") as f:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(f.read())

        encoders.encode_base64(attachment)

        filename = os.path.basename(pdf_path)
        attachment.add_header(
            "Content-Disposition",
            f"attachment; filename={filename}"
        )

        msg.attach(attachment)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to, msg.as_string())
        server.quit()

        return {
            'success': True
        }
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }