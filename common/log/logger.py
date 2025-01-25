import logging


def info(msg):
    logger = logging.getLogger('common')
    # logger.info(msg)


def debug(msg):
    logger = logging.getLogger('common')
    logger.debug(msg)


def error(msg):
    logger = logging.getLogger('common')
    logger.error(msg)
