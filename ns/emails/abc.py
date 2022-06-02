from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import getLogger
from os.path import basename
from smtplib import SMTP

from jinja2 import Environment, FileSystemLoader

logger = getLogger()


class EmailsABC:
    SMTP_HOST = None
    SMTP_PORT = None
    SMTP_EMAIL = None
    SMTP_LOGIN = None
    SMTP_PASSWORD = None
    TEMPLATES_PATH = None

    def _send_email(self, email: str, subject: str, text: str, text_type: str = 'plain', files: list[str] = None):
        message = MIMEMultipart()
        message['From'] = self.SMTP_EMAIL
        message['To'] = email
        message['Subject'] = subject
        message.attach(MIMEText(text, text_type))

        if files:
            for file_path in files:
                with open(file_path, "rb") as file:
                    part = MIMEApplication(
                        file.read(),
                        Name=basename(file_path)
                    )
                part['Content-Disposition'] = f'attachment; filename="{basename(file_path)}"'
                message.attach(part)
        message_text = message.as_string()

        server = SMTP(self.SMTP_HOST, self.SMTP_PORT)
        server.starttls()
        server.login(self.SMTP_LOGIN, self.SMTP_PASSWORD)
        server.sendmail(self.SMTP_EMAIL, email, message_text)

        logger.info(f'Email to "{email}" with subject "{subject}" sent')

    def _render_html(self, template_name: str, context: dict) -> str:
        env = Environment(loader=FileSystemLoader(self.TEMPLATES_PATH))
        template = env.get_template(template_name)
        return template.render(**context)


