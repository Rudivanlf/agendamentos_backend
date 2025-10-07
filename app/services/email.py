# app/services/email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..core.config import settings


def send_appointment_confirmation(
    recipient_email: str,
    client_name: str,
    agendamento_date: str,
    agendamento_descricao: str
):
    """Função síncrona para enviar o email usando smtplib."""

    # 1. Configura a mensagem
    sender_email = settings.SMTP_SENDER_EMAIL

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Agendamento Confirmado - {client_name}"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    # 2. Cria o corpo do email (pode ser HTML ou Plain Text)
    text = (
        f"Olá {client_name},\n\n"
        f"Seu agendamento foi confirmado para a data: {agendamento_date}.\n"
        f"Serviço: {agendamento_descricao}\n\n"
        "Obrigado por utilizar nossos serviços!"
    )

    html = f"""
    <html>
        <body>
            <h3>Confirmação de Agendamento</h3>
            <p>Olá <strong>{client_name}</strong>,</p>
            <p>Seu agendamento foi registrado com sucesso e está confirmado!</p>
            <p><strong>Detalhes:</strong></p>
            <ul>
                <li><strong>Data/Hora:</strong> {agendamento_date}</li>
                <li><strong>Cliente:</strong> {client_name}</li>
                {f'<li><strong>Serviço:</strong> {agendamento_descricao}</li>' if agendamento_descricao else ''}
            </ul>
            <p>Aguardamos você. Atenciosamente,<br>A Equipe.</p>
        </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    msg.attach(part1)
    msg.attach(part2)

    # 3. Envia o email
    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()  # Inicia a conexão segura (TLS)
            server.login(settings.SMTP_SENDER_EMAIL, settings.SMTP_PASSWORD)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"Email de confirmação enviado para: {recipient_email}")

    except Exception as e:
        # Em produção, você deve logar esse erro para investigação futura
        print(f"ERRO ao enviar email para {recipient_email}: {e}")
