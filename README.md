# Beautifully Simple Static [Bottle](http://bottlepy.org/) Blog Generator

## Why?
Because there aren't enough static website generators already in existence that 
look beautiful. 

This is one I created for (http://www.urunu.com](my personal blog) 
to learn how to build a Python website from scratch.  It's a bit of a hack but
it does the job perfectly for my needs. For simplicity and ease-of-learning, 
and following the Bottle design pattern, all of the Python code lives in one
file, [app.py](app.py)

If you're looking for a full-featured, well-written static file generator then
I would highly recommend [acrylamid](http://posativ.org/acrylamid/) over this
project.  

However if you want a starting-point for your own experiments in making websites 
and static sites in Python, this isn't the worst place that you could start.  

Check the [docs/TODO.md](docs/TODO.md) or [docs/ROADMAP.md](docs/ROADMAP.md) 
to see what's left to do and if you make some [docs/CHANGES.md](docs/CHANGES.md) I'll be
sure to add you to the [docs/CREDITS.md](docs/CREDITS.md) and [www/humans.txt](www/humans.txt) files.

### Features

* Generates static HTML files under the `www/blog/` from * [markdown](https://guides.github.com/features/mastering-markdown/) `content` file folder input
* Uses [Waitress WSCGI Server](http://docs.pylonsproject.org/projects/waitress/en/latest/index.html): it is pure-Python, standard library only, cross-platform, deployment-oriented, production-quality.
* Generated HTML is minified 
* Files in `/www/js/` when served

## Setup

* `pip install -r requirements.txt`
* edit `config.py` as needed

## Usage
Put markdown files in the folder `content/` ensuring that your markdown files use a content header:

e.g. `content/2015-12-25-xmas.md`

```
---
date: 2015-04-01 12:56
permalink: /blog/2015-04-01-cioran.html
title: Emil Cioran Quote
tags: [emil cioran, cioran, philosophy, quotes]
---
"I have all the defects of other people, and yet everything they do seems to me inconceivable."
Emil Cioran
```

### Command Line Interface
* The file `cli.py` is implemented using [click](http://click.pocoo.org/4/)

## Running

* `python app.py` 
* Browse the website at [http://localhost:8080](http://localhost:8080/)

All the files are generated at startup as html in the `www/blog/` folder.  The files 
in `www/` can then be synchronised with your website using a tool like [rsync](http://en.wikipedia.org/wiki/Rsync)

### Theming and Customisation
* Edit the `views/*.tpl` as needed for your website
* Edit the blog assets (css, js etc) in `www/`

## Documentation

* Everything's in the [docs/](docs/) folder.
