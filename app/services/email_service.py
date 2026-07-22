import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, render_template

logger = logging.getLogger(__name__)


def enviar_email(destinatario, assunto, corpo_html):
    smtp_host = current_app.config.get('SMTP_HOST', '')
    smtp_port = current_app.config.get('SMTP_PORT', 587)
    smtp_user = current_app.config.get('SMTP_USER', '')
    smtp_pass = current_app.config.get('SMTP_PASS', '')
    remetente = current_app.config.get('SMTP_FROM', smtp_user)

    if not smtp_host or not smtp_user or not smtp_pass:
        logger.warning('SMTP nao configurado. Email nao enviado para %s', destinatario)
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    parte_texto = MIMEText('Conteudo HTML nao suportado.', 'plain', 'utf-8')
    parte_html = MIMEText(corpo_html, 'html', 'utf-8')
    msg.attach(parte_texto)
    msg.attach(parte_html)

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(remetente, [destinatario], msg.as_string())
        logger.info('Email enviado para %s', destinatario)
        return True
    except Exception as e:
        logger.error('Erro ao enviar email para %s: %s', destinatario, e)
        return False
