from datetime import datetime
import os
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logger(name=__name__, log_dir="./"):
    '''
    usage:
        # In other_module.py import this module as follows
        import my_logger
        logger = my_logger.setup_logger(name='MyLogger', log_dir='/var/dum/logs/')

        logger.info('This is a log message saved by day. And with name MyLogger')

    *Log files seem to be saved with bytes type?*
    '''
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    try:
        logger = logging.getLogger(name)

        if not logger.hasHandlers():
            logger.setLevel(logging.DEBUG)
            fmt='[%(name)s] [%(asctime)s] [%(levelname)s] - %(message)s'

            # handler for log-file-name by everyday
            log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
            log_path = os.path.join(log_dir, log_filename)
            timed_file_handler = TimedRotatingFileHandler(log_path, when="D", interval=1, backupCount=30, encoding='utf-8')
            timed_file_handler.setFormatter(logging.Formatter(fmt))

            # handler for print out to console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(fmt))

            logger.addHandler(timed_file_handler)
            logger.addHandler(console_handler)

        return logger
    
    except Exception as e:
        print(f"Error setting up logger: {e}")
        raise


if __name__ == "__main__":
    logger = setup_logger()
    logger.debug("...debug...")
    logger.info("...info...")
    logger.warning("...warning...")
    logger.error("...error...")
    logger.critical("...critical...")
