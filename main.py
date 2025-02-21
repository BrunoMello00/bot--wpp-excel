import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import re
from time import sleep

# Função para formatar o número no padrão +5521XXXXXXXXX
def formatar_numero(numero):
    # Remover caracteres não numéricos
    numero_limpo = re.sub(r'\D', '', str(numero))
    
    # Adicionar código do país e DDD se necessário
    if len(numero_limpo) == 11 and numero_limpo.startswith('9'):
        return f"+5521{numero_limpo}"
    elif len(numero_limpo) == 11 and numero_limpo.startswith('21'):
        return f"+55{numero_limpo}"
    elif len(numero_limpo) == 13 and numero_limpo.startswith('5521'):
        return f"+{numero_limpo}"
    elif len(numero_limpo) == 9 and numero_limpo.startswith('9'):
        return f"+5521{numero_limpo}"
    elif len(numero_limpo) == 10 and numero_limpo.startswith('21'):
        return f"+5521{numero_limpo[2:]}"
    elif len(numero_limpo) == 8 and numero_limpo.startswith('9'):
        return f"+55219{numero_limpo}"
    else:
        raise ValueError(f"Número {numero} não está no formato esperado.")

# Configurações do Chrome
chrome_options = Options()
user_data_dir = os.path.join(os.getenv('TEMP'), 'chrome-profile')
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")  # Manter a sessão do WhatsApp Web
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--no-sandbox")  # Evitar problemas de sandbox
chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar problemas de memória
chrome_options.add_argument("--remote-debugging-port=9222")  # Habilitar debugging remoto
chrome_options.add_argument("--disable-gpu")  # Desabilitar GPU (útil para headless)

# Caminho do ChromeDriver (substitua pelo caminho correto)
chrome_driver_path = "D:/Projetos Pessoais/Bot WPP - Excel/chromedriver.exe"
service = Service(chrome_driver_path)

# Iniciar o navegador
driver = webdriver.Chrome(service=service, options=chrome_options)

# Abrir o WhatsApp Web
driver.get("https://web.whatsapp.com")
print("Por favor, escaneie o QR Code para logar no WhatsApp Web.")
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))

# Carregar o arquivo Excel
df = pd.read_excel('pg.xlsx')

# Acessar as colunas
nomes = df['Nome']
numeros = df['Numero']  # Certifique-se de que o nome da coluna está correto
links = df['Link']

# Função para enviar mensagem no WhatsApp
def enviar_whatsapp(nome, numero, link):
    mensagem = f"Oi {nome}.\nTudo bom?\nSegue o link para acesso ao prédio: {link}"
    try:
        # Formatar o número antes de enviar
        numero_formatado = formatar_numero(numero)
        
        # Abrir o chat com o número
        driver.get(f"https://web.whatsapp.com/send?phone={numero_formatado}")
        print(f"Tentando abrir o chat para {nome} ({numero_formatado})...")
        
        # Esperar até que a caixa de texto esteja presente
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))
            print(f"Chat aberto para {nome} ({numero_formatado}).")
        except Exception as e:
            print(f"Erro ao abrir o chat para {nome} ({numero_formatado}): {e}")
            return  # Sair da função se o chat não abrir

        # Localizar a caixa de texto e enviar a mensagem
        caixa_texto = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        caixa_texto.send_keys(mensagem)
        sleep(2)  # Esperar 2 segundos antes de enviar
        caixa_texto.send_keys(Keys.ENTER)  # Enviar a mensagem
        print(f"Mensagem enviada para {nome} ({numero_formatado})")
        
        # Esperar antes de enviar a próxima mensagem
        sleep(5)
    except Exception as e:
        print(f"Erro ao enviar mensagem para {nome} ({numero}): {e}")

# Enviar mensagens para todos os contatos
for nome, numero, link in zip(nomes, numeros, links):
    try:
        enviar_whatsapp(nome, numero, link)
    except ValueError as e:
        print(f"Erro ao formatar número {numero}: {e}")

# Fechar o navegador após o envio
driver.quit()