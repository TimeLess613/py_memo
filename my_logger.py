from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logger(name=__name__, level=logging.DEBUG, when="D", interval=1, backupCount=30, fmt='[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s'):
    '''
    usage:
        # In other_module.py import this module as follows
        from my_logger import logger
        logger.info('这是一条按天保存的日志信息。')
    '''

    try:
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # 动态生成日志文件名
        log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
        handler = TimedRotatingFileHandler(log_filename, when=when, interval=interval, backupCount=backupCount, encoding='utf-8')
        handler.setFormatter(logging.Formatter(fmt))

        logger.addHandler(handler)
        return logger
    except Exception as e:
        print(f"Error setting up logger: {e}")
        raise


logger = setup_logger()
