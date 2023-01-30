import os
import logging

from pythonjsonlogger import jsonlogger

from ddtrace import tracer

running_local = 'true'
try:
    running_local = os.environ.get('RUN_LOCAL')
except KeyError:
    running_local = 'false'

# This information will show up in a log search in the Datadog console
if running_local == 'false':
    FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
              '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
              '- %(message)s')

else:
    FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
              '- %(message)s')
    JSON_FORMAT = '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(levelname)s %(message)s')
log_handler.setFormatter(formatter)

logger.addHandler(log_handler)
logger.info('Log Message')
