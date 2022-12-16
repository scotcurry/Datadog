import os
import datetime
import logging

# from ddtrace import patch; patch(logging=True)
from flask import Flask, request, render_template
from ddtrace import tracer

app = Flask(__name__)
application = app
app.secret_key = 'UdGspIJlMFSIeyaRTrrI'

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

logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.level = logging.DEBUG

if running_local is None:
    log.debug('Running Local: FALSE')


@tracer.wrap()
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index_page():
    headers = request.headers
    user_agent = headers.get('HTTP_USER_AGENT')
    current_time = datetime.datetime.now()
    log.debug("Debug Messages - Don't show up in Indexes")
    log.info('INFO message - Do show up in indexes')

    return render_template('index.html', current_time=current_time, user_agent=user_agent)
