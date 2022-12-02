import subprocess
import sys

import click
import logging
from flask import Flask, json, request

api = Flask(__name__)
options = {}


@api.route('/qaqc/run', methods=['POST'])
def qaqc_run():
    d = request.json

    target = d.get('target')
    thing_uuid = d.get('thing_uuid')

    # calling tsm-extractor
    # see -> tsm-extractor/src/main.py [OPTIONS] command [ARGS]
    cmd = ['python3', '/home/appuser/app/src/main.py']
    if options['verbose']:
        cmd += ['-v']
    cmd += [
        'run-qaqc',
        '-t', target,
        '-d', thing_uuid,
        '-m', options['mqtt_broker'],
        '-u', options['mqtt_user'],
        '-pw', options['mqtt_password'],
    ]

    r = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    if r.returncode == 0:
        logging.info(f"successfully qcqa run for '{target}'")
    else:
        ctx = {
            'code': r.returncode,
            'err': r.stderr,
            'out': str(r.stdout),
        }
        logging.error(f"qaqc run failed. {ctx=}")

    return json.dumps({
        'code': r.returncode,
        'err': r.stderr,
        'out': str(r.stdout)
    }), 200 if r.returncode == 0 else 500


@api.route('/extractor/run', methods=['POST'])
def extractor_run():
    # parse -p AnotherCustomParser -t postgresql://postgres:postgres@postgres.example.com/postgres -s https://example.com/ -d ce2b4fb6-d9de-11eb-a236-125e5a40a845
    # python3 /home/appuser/app/src/main.py parse -p AnotherCustomParser -t postgresql://postgres:postgres@postgres.example.com/postgres -s https://example.com/ -d ce2b4fb6-d9de-11eb-a236-125e5a40a845
    # curl -v http://localhost:5000/extractor/run -d '{"parser":"AnotherCustomParser", "target":"postgresql://postgres:postgres@postgres/postgres", "source":"https://example.com/","thing_uuid":"ce2b4fb6-d9de-11eb-a236-125e5a40a845"}' -X POST -H "Content-Type: application/json"
    # curl -v http://extractor:5000/extractor/run -d '{"parser":"AnotherCustomParser", "target":"postgresql://postgres:postgres@postgres/postgres", "source":"https://example.com/","thing_uuid":"ce2b4fb6-d9de-11eb-a236-125e5a40a845"}' -X POST -H "Content-Type: application/json" | jq
    d = request.json

    parser = d.get('parser')
    target = d.get('target')
    source = d.get('source')
    thing_uuid = d.get('thing_uuid')

    # calling tsm-extractor
    # see -> tsm-extractor/src/main.py [OPTIONS] command [ARGS]
    cmd = ['python3', '/home/appuser/app/src/main.py']
    if options['verbose']:
        cmd += ['-v']
    cmd += [
        'parse',
        '-p', parser,
        '-t', target,
        '-s', source,
        '-d', thing_uuid,
        '-m', options['mqtt_broker'],
        '-u', options['mqtt_user'],
        '-pw', options['mqtt_password'],
    ]

    r = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    if r.returncode == 0:
        logging.info(f"successfully parsed '{source}'")
    else:
        ctx = {
            'code': r.returncode,
            'err': r.stderr,
            'out': str(r.stdout),
            'source': source,
            'parser': parser
        }
        logging.error(f"parsing failed. {ctx=}")

    return json.dumps({
        'code': r.returncode,
        'err': r.stderr,
        'out': str(r.stdout)
    }), 200 if r.returncode == 0 else 500


@click.command()
@click.option(
    'mqtt_broker', '--mqtt-broker', '-m',
    help="MQTT broker to connect. Explicitly pass 'None' to disable mqtt-logging feature.",
    required=True,
    show_envvar=True,
    envvar='MQTT_BROKER',
)
@click.option(
    'mqtt_user', '--mqtt-user', '-u',
    help='MQTT user',
    show_envvar=True,
    envvar='MQTT_USER'
)
@click.option(
    'mqtt_password', '--mqtt-password', '-pw',
    help='MQTT password',
    show_envvar=True,
    envvar='MQTT_PASSWORD'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help="Print more output.",
    envvar='VERBOSE',
    show_envvar=True,
)
def cli(mqtt_broker, mqtt_user, mqtt_password, verbose):

    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level)

    if mqtt_broker != "None":
        if mqtt_password is None:
            raise click.MissingParameter("mqtt_password", param_type='parameter')
        if mqtt_user is None:
            raise click.MissingParameter("mqtt_user", param_type='parameter')

    options.update(
        mqtt_broker=mqtt_broker,
        mqtt_user=mqtt_user,
        mqtt_password=mqtt_password,
        verbose=verbose
    )

    api.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    cli()
