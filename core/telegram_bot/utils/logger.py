import logging

# Создание логгера с именем текущего модуля
logger = logging.getLogger(__name__)

# Настройка формата и уровня логирования для консольных сообщений
logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s"
)

# Создание обработчика для записи логов в файл info.log
file_handler = logging.FileHandler(
    filename='info.log',
    encoding='utf-8'
)

# Настройка формата и уровня логирования для сообщений в файле
file_handler.setFormatter(
    logging.Formatter("%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s")
)

# Добавление обработчика к корневому логгеру
logging.getLogger().addHandler(file_handler)
