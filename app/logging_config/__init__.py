import logging
import os
import sys
from datetime import datetime


def configure_logging():
    env = os.getenv('ENV')

    if not os.path.exists('log'):
        os.mkdir('log')

    if not os.path.exists(f'log/{env}'):
        os.mkdir(f'log/{env}')

    log_time = '{:%Y-%m-%d_%H:%M:%S}'.format(datetime.now())
    log_path = f'log/{env}/{log_time}.log'

    logging.basicConfig(format='%(asctime)s [%(name)s] [%(levelname)s]: %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO,
                        handlers=[
                            logging.StreamHandler(stream=sys.stdout),
                            logging.FileHandler(
                                filename=log_path
                            )
                        ])
    logging.getLogger('watchfiles.main').setLevel(logging.WARNING)
    