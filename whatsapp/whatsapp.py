import os
from logger.logger import logger
from wrapper_vjwhats import WhatsApp
from selenium import webdriver

options = webdriver.ChromeOptions()
profile = "Default"
data_dir = os.path.join(
    os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User", "Data"
)
options.add_argument(f"--user-data-dir={data_dir}")
options.add_argument(f"--profile-directory={profile}")


def send_whatsapp(
    username, file, message="> Relatório de pagamentos gerado com sucesso!"
):
    """
    Envia uma mensagem e um arquivo via WhatsApp Web.
    :param file: Caminho do arquivo a ser enviado.
    :param message: Mensagem a ser enviada.
    """
    driver = webdriver.Chrome(options=options)
    try:
        whatsapp = WhatsApp(browser=driver)
        whatsapp.find_by_username(username)
        whatsapp.send_message(message)
        whatsapp.send_file(file, 1)
        logger.info(f" Mensagem enviada para {username} com sucesso!")
    except Exception as e:
        logger.critical(f"[ERROR] Ocorreu um erro ao enviar a mensagem: {e}")
    finally:
        driver.quit()
