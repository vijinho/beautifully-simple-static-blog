# Beautifully Simple Static [Bottle](http://bottlepy.org/) Blog Generator

## Why?
Because there aren't enough static website generators already in existence that 
look beautiful. 

This is one I created for [my personal blog](http://www.urunu.com)
to learn how to build a Python website from scratch.  It's a bit of a hack but
it does the job perfectly for my needs. For simplicity and ease-of-learning, 
and following the single-file Bottle design, all of the main web code lives in one
file, [app.py](app.py) 

If you're looking for a full-featured, well-written static file generator then
I would highly recommend [acrylamid](http://posativ.org/acrylamid/) over this
project.  

However if you want a starting-point for your own experiments in making websites 
and static sites in Python, this isn't the worst place that you could start.  

Check the [TODO.md](docs/TODO.md) or [ROADMAP.md](docs/ROADMAP.md) 
to see what's left to do and if you make some [CHANGES.md](docs/CHANGES.md) I'll be
sure to add you to the [CREDITS.md](docs/CREDITS.md) and [humans.txt](www/humans.txt) files.

### Features

* No database required
* Generates static HTML files under the [www/blog/](www/blog) from * [markdown](https://guides.github.com/features/mastering-markdown/) [content](content) files folder input
* Uses [Waitress WSCGI Server](http://docs.pylonsproject.org/projects/waitress/en/latest/index.html): it is pure-Python, standard library only, cross-platform, deployment-oriented, production-quality.
* Generated HTML is optionally minified and saved to webroot
* JS files in [/www/js/](www/js) optionally minified when served direct
* Caching, minification and static files can be disabled

## Setup

* `pip install -r requirements.txt`
* Copy config file: `cp config.py.example config.py`
* Edit `config.py` as needed

### config.py explanation

```
CONFIG = {
    'debug': False,                  # debug mode
    'generate_static_files': True,   # generate static website files
    'minify_js': True,               # minify javascript served by webserver (not static files)
    'minify_html': True,             # minify all output html including static files
    'cache': True,                   # cache files and output of app
    'cache_dir': 'tmp/cache/',       # default location of cached files
    'content_dir': 'content/',       # default location of .md blog content files
    'docs_dir': 'docs/',             # default location for .md docs generated in www/blog/docs displayed under `meta` on the homepage
    'web_dir': 'www/',               # default location of website root directory
    'blog_dir': 'www/blog/',         # default location of webroot for blog
    'js_dir': 'www/js/',             # default location of javascript files
    'title': 'urunu',                # name of the blog
    'author': 'Vijay Mahrra'         # author of the blog
}
```

## Usage
Put markdown files in the folder [content/](content/) ensuring that your markdown files use a content header:

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
* The file [cli.py](cli.py) is implemented using [click](http://click.pocoo.org/4/) (TO BE DONE!)

## Running

* `python app.py` 
* Browse the website at [http://localhost:8080](http://localhost:8080/)

All the .html files are generated at startup as html in the [www/blog](www/blog) and [www/blog/docs](www/blog/docs) folders.  
The files in [www](www/) can then be synchronised with your website using a tool like [rsync](http://en.wikipedia.org/wiki/Rsync)

### Theming and Customisation

* Change the [view](views/)*.tpl as needed for your website
* Docs for 'Meta' information on the right column are generated from the files in [docs/](docs) folder.
* Error 404 File Not Found page: [www/error/404.html](www/error/404.html) - see [www/.htaccess](.htaccess) file for how to use with apache.
* Edit the css in [www/css/](www/css/)
* Edit the javascript in [www/js/](www/js/)
* Put images in [www/img/](www/img/)
* Favourite icons: [www/favicon.ico](www/favicon.ico) and [www/img/favicon.png](www/img/favicon.png)
* Don't forget to update [www/humans.txt](www/humans.txt)!

## Documentation

* Everything's in the [docs/](docs/) folder.
