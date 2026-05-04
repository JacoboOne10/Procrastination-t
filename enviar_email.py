import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_REMITENTE, EMAIL_PASSWORD


def generar_codigo():
    return str(random.randint(100000, 999999))


def enviar_codigo_verificacion(correo_destino, codigo):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_REMITENTE
        msg["To"] = correo_destino
        msg["Subject"] = "Código de verificación - Procrastination't"

        cuerpo = f"""
Hola 👋

Tu código de verificación para completar el registro es:

        {codigo}

Este código es de un solo uso. Si no solicitaste este registro, ignora este mensaje.

— Procrastination't
        """
        msg.attach(MIMEText(cuerpo, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
            servidor.sendmail(EMAIL_REMITENTE, correo_destino, msg.as_string())

        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False