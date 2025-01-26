import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Função para enviar email
def enviar_email(solicitante, cargo, equipamento, local):
    remetente = 'landimfabiano01@gmail.com'  # Substitua com seu e-mail
    destinatario = 'flpiratesofcaribbean@gmail.com'  # Corrigido para um e-mail válido
    senha = 'LFG44gl2C4nt1'  # Substitua com a senha de app gerada (se necessário)

    # Definindo o assunto e corpo do e-mail
    assunto = 'Ordem de Serviço Solicitada'
    corpo = f"""
    Ordem de Serviço:

    Solicitante: {solicitante}
    Cargo: {cargo}
    Equipamento: {equipamento}
    Local: {local}
    Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    """

    # Configuração do servidor SMTP (exemplo usando Gmail)
    try:
        # Conectando ao servidor SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Ativa a criptografia para proteger a senha

        # Login na conta
        server.login(remetente, senha)

        # Construção da mensagem
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto

        msg.attach(MIMEText(corpo, 'plain'))

        # Envia o e-mail
        server.sendmail(remetente, destinatario, msg.as_string())
        server.quit()  # Fecha a conexão com o servidor

        return True  # Se o envio for bem-sucedido
    except smtplib.SMTPAuthenticationError:
        print("Erro de autenticação. Verifique sua senha de aplicativo ou as configurações de segurança da sua conta.")
        return False
    except smtplib.SMTPException as e:
        print(f"Erro ao enviar o e-mail: {e}")
        return False

# Teste da função de envio de email
if enviar_email('Fabiano', 'Desenvolvedor', 'Computador', 'Escritório'):
    print("E-mail enviado com sucesso!")
else:
    print("Falha ao enviar e-mail.")
