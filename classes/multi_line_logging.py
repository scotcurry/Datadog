import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d %(message)s')
log_handler.setFormatter(formatter)

working_directory = os.getcwd()
if 'scot.curry' in working_directory:
    running_on_mac = True
    file_logger = logging.getLogger(__name__)
    file_logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('./logs/datadog.log')
    file_handler.setFormatter(formatter)
    file_logger.addHandler(file_handler)

logger.info('--- Logging Entry from multi-line-logger class ---')


def write_multi_line_log_entry():
    log_message = build_log_message(5000, True)
    logger.info(log_message)
    if running_on_mac:
        file_logger.info(log_message)


def build_log_message(total_lines, allow_blanks):

    log_text = '--- Syntax <api url>/api/multi_line_log?number_of_lines_=<xx>&allow_blanks=<Y|N> ---\n'
    log_text = log_text + '--- where number_of_lines and allow blanks are optional.  ---\n'
    log_text = log_text + '--- Default of 10 lines not blanks.  Blanks will be every 5 lines. ---\n'
    for count in range(total_lines):
        log_text = log_text + 'Line: ' + str(count) + '\n'
        if allow_blanks:
            if (count % 5) == 0:
                log_text = log_text + '\n'

    base_array = ['Scot', 'Otis', 'Lola']
    try:
        error_value = base_array[4]
        print(error_value)
    except IndexError as index_exception:
        logger.exception('Index Error Caught')
        if running_on_mac:
            file_logger.exception('Index Error Caught')

    return log_text