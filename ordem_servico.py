import PySimpleGUI as sg
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

# Função para enviar email
def enviar_email(solicitante, cargo, equipamento, local, resumo):
    remetente = 'flpiratesofcaribbean@gmail.com'  # Substitua com seu e-mail
    destinatario = 'landimfabiano01@gmail.com'  # Substitua com o e-mail do destinatário
    
    # Carregar a senha de app de uma variável de ambiente (método mais seguro)
    senha = os.getenv('EMAIL_APP_PASSWORD')  # Verifique se a variável de ambiente foi configurada
    
    if not senha:
        sg.popup_error("Senha de aplicativo não configurada.")
        return False
    
    # Definindo o assunto e corpo do e-mail
    assunto = 'Ordem de Serviço Solicitada'
    corpo = f"""
    Ordem de Serviço:

    Solicitante: {solicitante}
    Cargo: {cargo}
    Equipamento: {equipamento}
    Local: {local}
    Resumo: {resumo}
    Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    """

    try:
        # Conectando ao servidor SMTP (usando Gmail como exemplo)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Ativa a criptografia para proteger a senha

        # Login na conta
        server.login(remetente, senha)

        # Construção da mensagem
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto

        # Adicionando o corpo do e-mail
        msg.attach(MIMEText(corpo, 'plain'))

        # Enviando o e-mail
        server.sendmail(remetente, destinatario, msg.as_string())
        server.quit()  # Fecha a conexão com o servidor

        sg.popup("E-mail enviado com sucesso!")
        return True
    
    except smtplib.SMTPAuthenticationError:
        sg.popup_error("Erro de autenticação. Verifique sua senha de aplicativo ou as configurações de segurança da sua conta.")
    except smtplib.SMTPConnectError:
        sg.popup_error("Erro ao conectar com o servidor SMTP. Verifique sua conexão de rede.")
    except smtplib.SMTPException as e:
        sg.popup_error(f"Erro ao enviar o e-mail: {e}")
    except Exception as e:
        sg.popup_error(f"Ocorreu um erro inesperado: {e}")
    
    return False

# Layout da interface PySimpleGUI
sg.theme('Dark Blue')
layout = [
    [sg.Text('Solicitante'), sg.InputText(key='solicitante')],
    [sg.Text('Cargo'), sg.InputText(key='cargo')],
    [sg.Text('Equipamento'), sg.InputText(key='equipamento')],
    [sg.Text('Local'), sg.InputText(key='local')],
    [sg.Text('Resumo'), sg.Multiline(key='resumo', size=(50, 6))],
    [sg.Button('ENVIAR'), sg.Button('LIMPAR'), sg.Button('SAIR')]
]

# Criação da janela
window = sg.Window('Formulário de Ordem de Serviço', layout)

# Loop de eventos
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'SAIR':
        break

    if event == 'ENVIAR':
        # Coletando os dados inseridos no formulário
        solicitante = values['solicitante']
        cargo = values['cargo']
        equipamento = values['equipamento']
        local = values['local']
        resumo = values['resumo']
        
        # Validação dos campos obrigatórios
        if not all([solicitante, cargo, equipamento, local, resumo.strip()]):
            sg.popup("Por favor, preencha todos os campos, incluindo o Resumo!")
        else:
            # Chamando a função para enviar o e-mail
            enviar_email(solicitante, cargo, equipamento, local, resumo)

    if event == 'LIMPAR':
        # Limpar os campos do formulário
        window['solicitante'].update('')
        window['cargo'].update('')
        window['equipamento'].update('')
        window['local'].update('')
        window['resumo'].update('')

# Fechando a janela
window.close()