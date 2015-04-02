# -*- coding: utf-8 -*-
'''
Beautifully Simple Static Bottle Blog Generator
===============================================

Command Line Interface
'''

import click

# setup config passing storage
class Config(object):

    def __init__(self):
        self.verbose = False

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('-v', '--verbose', is_flag=True)
@click.option('-l', '--logfile', type=click.File('w'), required=False)
@pass_config
def cli(config, verbose, logfile):
    config.verbose = verbose
    config.logfile = logfile
    if config.verbose:
        click.secho('Verbose mode: Enabled',
                    fg='white', bold=True, reverse=True, blink=True)

if __name__ == '__main__':
    cli()
