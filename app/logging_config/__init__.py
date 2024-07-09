import logging
import os
import sys
from datetime import datetime

suppress_logs = [
    "watchfiles.main",
    "chromadb.config",
    "urllib3.connectionpool"
]


def configure_logging():
    log_path = __get_log_path()
    log_level = __get_log_level()

    logging.basicConfig(format='%(asctime)s [%(name)s] [%(levelname)s]: %(message)s',
                        datefmt='%H:%M:%S',
                        level=log_level,
                        handlers=[
                            logging.StreamHandler(stream=sys.stdout),
                            logging.FileHandler(
                                filename=log_path
                            )
                        ])
    for log in suppress_logs:
        logging.getLogger(log).setLevel(logging.WARNING)


def __get_log_path():
    env = os.getenv('ENV')

    if not os.path.exists('log'):
        os.mkdir('log')

    if not os.path.exists(f'log/{env}'):
        os.mkdir(f'log/{env}')

    log_time = '{:%Y-%m-%d_%H:%M:%S}'.format(datetime.now())
    log_path = f'log/{env}/{log_time}.log'

    return log_path


def __get_log_level():
    level = os.getenv('LOG_LEVEL')
    if not level or level == "INFO":
        return logging.INFO

    return logging.DEBUG
