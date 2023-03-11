import uuid
import json
from flask import Flask, url_for, render_template, redirect, abort, request, send_from_directory
from services.sqs_service import get_sqs, create_sqs, delete_sqs, initial_setup
from services.ec2_service import check_ssh_security


app = Flask(__name__, static_folder='templates/static', template_folder='templates')
app.debug = app.config["DEBUG"]


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@ app.route('/ec2', methods=['GET'])
def ec2():
    status = check_ssh_security()
    return json_response(status)

@ app.route('/dashboard', methods=['GET'])
def dashboard():
    result = get_sqs()
    return json_response({'service_name': result['name'], 'attrs': result['attrs']})

@ app.route('/manifest.json', methods=['GET'])
def manifest():
    return send_from_directory('templates', 'manifest.json')

@ app.route('/favicon.png', methods=['GET'])
def favicon():
    return send_from_directory('templates', 'favicon.png')

@ app.route('/cf_setup', methods=['GET'])
def cf_setup():
    result = initial_setup()
    return redirect(url_for('index'))

@ app.route('/create', methods=['GET'])
def create():
    r = request
    account = list(r.values.keys())[0]
    name = f'NewSQS_{uuid.uuid4()}'
    result = create_sqs(name, account)
    return redirect(url_for('index'))

@ app.route('/delete', methods=['POST'])
def delete():
    r = request
    url = list(r.values.keys())[0]
    result = delete_sqs(url)
    return redirect(url_for('index'))

@ app.route('/test-react', methods=['GET'])
def ilgor():
    d = {'isReactWorking': 'yes', 'isAwsWorking': 'yes'}
    return json_response(d)

def json_response(payload, status=200):
    return (json.dumps(payload), status, {'content-type': 'application/json'})


if __name__ == '__main__':
    app.run()
