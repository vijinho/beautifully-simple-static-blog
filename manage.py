#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Beautifully Simple Static Bottle Blog Generator
===============================================
Command Line Interface using Click http://click.pocoo.org/
"""
import os
import click

from builtins import *

__author__ = "Vijay Mahrra"
__copyright__ = "Copyright 2015, Vijay Mahrra"
__credits__ = ["Vijay Mahrra"]
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Vijay Mahrra"
__email__ = "vijay.mahrra@gmail.com"
__status__ = "Development"

@click.group()
@click.option('-v', '--verbose', count=True, help='Set the level of verbosity.')
def cli():
    print('Verbosity is: {0}'.format(verbose))

@cli.command()
@click.option('-v', '--verbose', count=True, help='Set the level of verbosity.')
def generate(verbose):
    pass

@cli.command()
def serve(verbose):
    pass

@cli.command()
def newpost(verbose):
    pass

@cli.command()
def newpage(verbose):
    pass

def yelp():
    cli()

if __name__ == '__main__':
    os.environ.setdefault("BASEDIR", os.path.abspath(os.path.join(os.path.dirname( __file__ ))))
    yelp()
