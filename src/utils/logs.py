import logging
import os
from datetime import datetime

date_str = datetime.now().strftime("%Y%m%d")
log_file = f'logs/{date_str}_Logging_Binance-Insider.log'

def configure_logging(log_level=logging.INFO):
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            pass

    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=log_file, level=log_level, format=log_format)

configure_logging()

def add_log(message, level=logging.INFO):
    logger = logging.getLogger(__name__)
    
    if level == logging.DEBUG:
        logger.debug(message)
    elif level == logging.INFO:
        logger.info(message)
    elif level == logging.WARNING:
        logger.warning(message)
    elif level == logging.ERROR:
        logger.error(message)
    elif level == logging.CRITICAL:
        logger.critical(message)
    else:
        logger.info(message)
