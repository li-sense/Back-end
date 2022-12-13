from loguru import logger
from sys import stderr



def logging_config():
    logger.remove()

    logger.add(
        "logs_testes.txt",
        format='{time} <r>{level}</r> <g>{message}</g> {file}',
        level='INFO',
    )

    logger.critical('senha')
    logger.debug('Debug')
    logger.info('Info')
    logger.warning('Warning')

if __name__ == '__main__':
    logging_config()


"""
from logging import Filter, Formatter, FileHandler
from loguru import logger
from sys import stderr


logger.remove()

logger.add(
    sink=stderr,
    format='{time} <r>{level}</r> <g>{message}</g> {file}',
    level='INFO',
)


def logging_config():
    logger.critical('senha')
    logger.debug('Debug')
    logger.info('Info')
    logger.warning('Warning')



"""