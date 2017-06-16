import logging
import sys

import click

from gitlab import GLSession


@click.command()
@click.option('--gitlab-server', envvar='GITLAB_SERVER', required=True)
@click.option('--gitlab-token', envvar='GITLAB_TOKEN', required=True)
@click.option('--gitlab-hook-url', envvar='GITLAB_HOOK_URL', required=True)
@click.option('--debug/--no-debug', '-d', help='debug logging')
def process_events(gitlab_server, gitlab_token, gitlab_hook_url, debug=False):
    """Simple program that shows last events from gitlab queue."""
    global gitlab, hook_url
    hook_url = gitlab_hook_url
    gitlab = GLSession(gitlab_server, gitlab_token)
    if debug:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    for proj in gitlab.getAllProjects():
        gitlab.setupHook(proj['id'], hook_url)

if __name__ == '__main__':
    process_events()
