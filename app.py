import datetime

from flask import Flask, request, render_template


app = Flask(__name__)
application = app
app.secret_key = 'UdGspIJlMFSIeyaRTrrI'


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index_page():
    current_time = datetime.datetime.now()
    return render_template('index.html', current_time=current_time)
