from flask import Flask, request
import json
from icinga2api.client import Client
import logging

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)


@app.route('/', methods=['POST'])
def pagerduty():
    data = json.loads(request.data)
    alert = data['messages'][0]['incident']['title'].split(" ")
    host = alert[3].replace("'", "")
    service = alert[1].replace("'", "")
    status = data['messages'][0]['event']
    owner = data['messages'][0]['incident']['assignments'][0]['assignee']['summary']
    comment = "{0} has acknowledged via PagerDuty".format(owner)

    if status == "incident.acknowledge":
        app.logger.info(data)
        if host == "DOWN":
            app.logger.info("{0} for host {1} being DOWN".format(comment, service))
            _ack_host(comment=comment, service=host)
        else:
            app.logger.info("{0} for {1} on {2}".format(comment, service, host))
            _ack_service(host=host, service=service, comment=comment)
    return "OK"


def _ack_service(host, service, comment):
    client = Client(config_file='/opt/icinga2api/local.conf')

    client.actions.acknowledge_problem(
        'Service',
        r'match("%s", host.name) && service.name=="%s"' % (host, service),
        'icingaadmin',
        comment,
        sticky=True)


def _ack_host(host, comment):
    client = Client(config_file='/opt/icinga2api/local.conf')

    client.actions.acknowledge_problem(
        'Host',
        r'match("{0}", host.name)'.format(host),
        'icingaadmin',
        comment)


if __name__ == "__main__":
    pagerduty.run()
