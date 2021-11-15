import subprocess

from flask import Flask, json, request

api = Flask(__name__)


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

    r = subprocess.run(
        ['python3', '/home/appuser/app/src/main.py', 'parse', '-p', parser, '-t', target, '-s',
         source,
         '-d', thing_uuid],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    return json.dumps({
        'code': r.returncode,
        'err': r.stderr,
        'out': str(r.stdout)
    }), 200 if r.returncode == 0 else 500


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5000)
