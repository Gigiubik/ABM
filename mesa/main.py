import sys
import os
import importlib
import click

PROJECT_PATH = click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True)


@click.group()
def cli():
    'Manage Mesa projects'


@cli.command()
@click.argument('project', type=PROJECT_PATH, default='.')
def run(project):
    '''Run mesa project PROJECT

    PROJECT is the path to the directory containing `run.py`, or the current
    directory if not specified.
    '''
    sys.path.insert(0, project)
    os.chdir(project)
    run = importlib.import_module('run')
    run.server.launch()
