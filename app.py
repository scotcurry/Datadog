import datetime
import logging
import sys

# from ddtrace import patch; patch(logging=True)
from flask import Flask, request, render_template
from ddtrace import tracer

app = Flask(__name__)
application = app
app.secret_key = 'UdGspIJlMFSIeyaRTrrI'

# This information will show up in a log search in the Datadog console
if sys.gettrace() is None:
    FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
              '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
              '- %(message)s')
else:
    FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
              '- %(message)s')

logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.level = logging.INFO

# tracer.configure(
#     # This needs to match the container_name field in the docker-compose.yaml file for Docker
#     # TODO:  Need to add the information for k8s when I get it built.
#     hostname='ddmac',
#     port=8126
# )


@tracer.wrap()
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index_page():
    headers = request.headers
    # user_agent = headers.environ['HTTP_USER_AGENT']
    user_agent = headers.get('HTTP_USER_AGENT')
    current_time = datetime.datetime.now()
    log.info('Application starting with user-agent: %s', user_agent)

    log.info('Another log Info')
    try:
        span = tracer.current_span()
        if span:
            span_name = span.name
            log.info('Span Name: ' + span_name)
        else:
            log.error('No span found')
    except:
        log.error('Exception in tracer.current_span()')

    if span is None:
        log.error('--- No span object ---')

    correlation_ids = (span.trace_id, span.span_id) if span else (None, None)
    return render_template('index.html', current_time=current_time)
