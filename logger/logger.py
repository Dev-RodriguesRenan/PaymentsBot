import datetime
import logging
import os
import sys
import colorama

colorama.init(autoreset=True)
# Configurando o diretório de logs
logs_directory = "logs"
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)
# Definir cores para cada nível de log
LOG_COLORS = {
    "DEBUG": colorama.Fore.BLUE,
    "INFO": colorama.Fore.GREEN,
    "WARNING": colorama.Fore.YELLOW,
    "ERROR": colorama.Fore.RED,
    "CRITICAL": colorama.Fore.MAGENTA,
}

# Definindo o formato do log
LOG_FORMAT = (
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    "%Y-%m-%d %H:%M:%S",
)


# Definindo o formato do log com cores
class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, colorama.Fore.WHITE)
        log_message = super().format(record)
        return f"{log_color}{log_message}"


# Criando o logger
logger = logging.getLogger("logger")
# Definindo o nível de log
logger.setLevel(logging.DEBUG)
# Criando um formato customizado para o log
formatter = CustomFormatter(*LOG_FORMAT)

# Console Handler (Saída no terminal)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# File Handler (Saída em arquivo)
file_handler = logging.FileHandler(
    f"{logs_directory}/app_{os.getpid()}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)
file_handler.setFormatter(
    logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s")
)

# Adicionar handlers ao logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
