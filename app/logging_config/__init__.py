import logging
import os
import sys
from datetime import datetime


def configure_logging():
    if not os.path.exists('log'):
        os.mkdir('log')
    
    logging.basicConfig(format='%(asctime)s [%(name)s] [%(levelname)s]: %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO,
                        handlers=[
                            logging.StreamHandler(stream=sys.stdout),
                            logging.FileHandler(filename='log/{:%Y-%m-%d_%H:%M:%S}.log'.format(datetime.now()))
                        ])
    logging.getLogger('watchfiles.main').setLevel(logging.WARNING)
    