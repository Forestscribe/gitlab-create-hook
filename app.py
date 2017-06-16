import logging
import sys

import click

import bson
from gitlab import GLSession
from kafka import KafkaConsumer

gitlab = None
hook_url = None


def do_event(event):
    if event.get('event_name') == 'project_create':
        gitlab.setupHook(event.get("project_id"), hook_url)


@click.command()
@click.option('--kafka-server', envvar='KAFKA_SERVER', required=True)
@click.option('--gitlab-server', envvar='GITLAB_SERVER', required=True)
@click.option('--gitlab-token', envvar='GITLAB_TOKEN', required=True)
@click.option('--gitlab-hook_url', envvar='GITLAB_HOOK_URL', required=True)
@click.option('--debug/--no-debug', '-d', help='debug logging')
def process_events(kafka_server, gitlab_server, gitlab_token, gitlab_hook_url, debug=False):
    """Simple program that shows last events from gitlab queue."""
    global gitlab, hook_url
    hook_url = gitlab_hook_url
    gitlab = GLSession(gitlab_server, gitlab_token)
    if debug:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    consumer = KafkaConsumer('gitlabbson', group_id="createhook", fetch_max_wait_ms=10000,
                             bootstrap_servers=[kafka_server])
    for event in consumer:
        do_event(bson.loads(event.value))

if __name__ == '__main__':
    process_events()
