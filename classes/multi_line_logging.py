import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(levelname)s %(message)s')
log_handler.setFormatter(formatter)

logger.addHandler(log_handler)
logger.info('--- Logging Entry from multi-line-logger class ---')


def write_multi_line_log_entry(log_message):
    logger.info(log_message)