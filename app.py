import json
import os
import datetime
import logging
import random

import requests

from classes.multi_line_logging import write_multi_line_log_entry
from classes.json_logging import write_json_log_entry

# from ddtrace import patch; patch(logging=True)
from flask import Flask, request, render_template, url_for
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
log.level = logging.INFO

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


@app.route('/chuckjoke', methods=['GET'])
def print_chuck_joke():
    response = requests.get('https://p4o643dcn3.execute-api.us-east-1.amazonaws.com/Prod/hello')
    body = response.content
    body = body.decode()
    body = body.replace('\\n', '')
    body = body.replace('\\"', '"')
    body = body.replace('"{', '{')
    body = body.replace('}"', '}')

    joke_json = json.loads(body)
    joke_text = joke_json['message']['joke_text']
    joke_number = joke_json['message']['joke_number']

    print(joke_text)
    print(body)

    log.info('Show Chuck Joke Number: ' + str(joke_number))
    chuck_image_location = './static/images/chuck_norris.png'

    current_time = datetime.datetime.now()
    return render_template('chuckjoke.html', current_time=current_time, joke_text=joke_text,
                           chuck_image=chuck_image_location)


@app.route('/api/chuck_joke', methods=['GET'])
def chuck_joke_api():
    response = requests.get('https://p4o643dcn3.execute-api.us-east-1.amazonaws.com/Prod/hello')
    body = response.content
    body = body.decode()
    body = body.replace('\\n', '')
    body = body.replace('\\"', '"')
    body = body.replace('"{', '{')
    body = body.replace('}"', '}')

    api_status_number = random.randint(1, 110)

    joke_json = json.loads(body)
    joke_id = joke_json['message']['joke_id']
    joke_text = joke_json['message']['joke_text']
    joke_number = joke_json['message']['joke_number']
    joke_dict = {'joke_status': api_status_number, 'joke_id': joke_id, 'joke_text': joke_text,
                 'joke_number': joke_number}
    joke_json = json.dumps(joke_dict)
    log.debug('DEBUG: ' + joke_json)
    log.info('--- Returning Chuck Joke: ' + str(api_status_number))
    return joke_json


@app.route('/logging_functions', methods=['GET', 'POST'])
def logging_functions_menu():
    current_time = datetime.datetime.now()
    if request.method == 'POST':
        if request.form.get('json_logging'):
            write_json_log_entry('JSON Log Entry')
            return render_template('logging_calls.html', current_time=current_time, post_method="JSON")
        elif request.form.get('multi_line_log'):
            write_multi_line_log_entry()
            return render_template('logging_calls.html', current_time=current_time, post_method="MULTI_LINE")
    elif request.method == 'GET':
        post_method = 'GET'
        return render_template('logging_calls.html', current_time=current_time, post_method=post_method)


@app.route('/multi_line_log', methods=['GET'])
def multi_line_log_api():
    total_lines = request.args.get('number_of_lines', default=10, type=int)
    allow_blanks = request.args.get('allow_blanks', default=False, type=bool)
    log_text = '--- Syntax <api url>/api/multi_line_log?number_of_lines_=<xx>&allow_blanks=<Y|N> ---\n'
    log_text = log_text + '--- where number_of_lines and allow blanks are optional.  ---\n'
    log_text = log_text + '--- Default of 10 lines not blanks.  Blanks will be every 5 lines. ---\n'
    for count in range(total_lines):
        log_text = log_text + 'Line: ' + str(count) + '\n'
        if allow_blanks:
            if (count % 5) == 0:
                log_text = log_text + '\n'

    write_multi_line_log_entry()
    return render_template('logging_calls.html')


@app.route('/database_functions', methods=['GET'])
def database_functions():
    response = requests.get('https://win2019server.curryware.org/api/database')
    body = response.content
    json_body = json.loads(body)
    sql_server_image_location = './static/images/sql_server.png'
    state_tax_rates = json_body['stateSalesTaxList']

    return render_template('state_tax.html', sql_image=sql_server_image_location, state_tax_rates=state_tax_rates)


@app.route('/random_error', methods=['GET'])
def random_error():
    random_value = random.randint(0, 99)
    if random_value < 5:
        divisor = 0
        log_text = 'Page is going to throw and error, return value was ' + str(random_value)
        log.error(log_text)
        return_value = 100 / divisor
    else:
        log_text = 'Lucky! no error, return value was ' + str(random_value)
        return_value = random_value

    return render_template('random_error.html', returned_value=return_value)


@app.route('/forced_error', methods=['GET'])
def forced_error():
    divisor = 0
    log_text = "This page forced an error"
    log.error(log_text)
    return_value = 100 / divisor

    return render_template('random_error.html', return_value=return_value)


@app.route('/azure_container_app', methods=['GET'])
def azure_container_app():
    site_url = 'https://curryware-rssfeedpuller.jollyforest-507ca08d.northcentralus.azurecontainerapps.io/rssfeedpuller'
    try:
        response = \
            requests.get(site_url)
        json_body = json.loads(response.content)
        azure_icon_image = '/static/images/azure_icon.png'
        rss_feeds = json_body['feedList']
    except requests.exceptions.ConnectionError:
        return render_template(site_url)

    return render_template('azure_container_app.html', rss_feeds=rss_feeds, azure_icon_image=azure_icon_image)
