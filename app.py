# -*- coding: utf-8 -*-

import os
import sys
import htmlmin
from jsmin import jsmin
import markdown
import pickle
import hashlib
from datetime import date
import config
from bottle import error, route, get, static_file, template, default_app, run

# fix for bad encoding reading files
reload(sys)
sys.setdefaultencoding('utf8')

def make_hash(key):
    """Generate a string hash from a given key string"""
    key = hashlib.md5(key)
    return key.hexdigest()

def cache_set(key, data):
    """Save an item of data to the cache - return boolean success"""
    try:
        filename = "tmp/cache/{key}.tmp".format(key = make_hash(key))
        pickle.dump(data, open(filename, "wb"))
        return True
    except IOError:
        return False

def cache_get(key):
    """Get an item of data from the cache - return data or empty dict"""
    try:
        filename = "tmp/cache/{key}.tmp".format(key = make_hash(key))
        data = pickle.load(open(filename, "rb"))
        return data
    except IOError:
        return {}

def cache_remove(key):
    """Remove an item of data from the cache - return boolean success"""
    try:
        filename = "tmp/cache/{key}.tmp".format(key = make_hash(key))
        os.remove(filename)
        return True
    except OSError:
        return False
    except IOError:
        return False

def cache_clear():
    """Wipe the cache - return boolean success"""
    files = get_files_by_ext('.tmp', 'tmp/cache', cache = False)
    try:
        for filename,filepath in files.iteritems():
            os.remove(filepath)
    except OSError:
        pass
    except IOError:
        pass
    return True

def parse_markdown(text):
    """Return text contents as (str html5, dict meta-information, str original markdown)"""
    md = markdown.Markdown(output_format = 'html5', extensions = ['markdown.extensions.meta'])
    html = md.convert(text)
    meta = {}
    for k,v in md.Meta.iteritems():
        v = "".join(v)
        if k == 'tags':
            v = v[1:-1]
        meta[k] = v
    return html, meta, text

def parse_markdown_file(filepath):
    """Read a file name and return contents as str html5, dict meta-information, original markdown"""
    with open(filepath) as fh:
        text = fh.read()
        return parse_markdown(text)

def get_files_by_ext(filetype, filepath, cache = True):
    """Return a dict of all files of a given file extension"""
    cache_key = filetype + filepath
    matches = cache_get(cache_key)
    if cache is False or matches is False or len(matches) is 0:
        matches = {}
        files = []
        for root, dirs, files in os.walk(filepath):
            for file in files:
                if file.endswith(filetype):
                    path = os.path.join(root, file)
                    matches[file] = str(path)
        cache_set(cache_key, matches)
    return matches

def get_blog_posts_meta(cache = True, generate_static_html = False):
    """Return a dict of meta-information for all blog posts and generate static html files in www"""
    cache_key = 'blog_posts_meta'
    data = cache_get(cache_key)
    if cache is False or data is False or len(data) is 0:
        documents = get_files_by_ext('.md', 'content')
        for filename, filepath in documents.items():
            filepath = documents[filename]
            html, meta, document = parse_markdown_file(filepath)
            meta['filename'] = filename
            meta['filepath'] = filepath
            data[filename] = meta
            if generate_static_html is True:
                blog_markdown_to_html(filename) # generate all html files
            cache_set(cache_key, data)
    return data

def generate_static_website():
    """Generate static html files and website"""
    index()
    return get_blog_posts_meta(cache = False, generate_static_html = True)

def generate_page(data = {}, tpl = 'default', header = 'header.tpl', footer = 'footer.tpl', minify = True, outfile = None):
    """Render a multiple templates using the same data dict for header, body, footer templates """
    html = template(header, data = data) + template(tpl, data = data) + template(footer, data = data)
    if minify is True:
        html = htmlmin.minify(html,
            remove_comments = True,
            remove_all_empty_space = True,
            reduce_empty_attributes = True,
            reduce_boolean_attributes = True,
            remove_optional_attribute_quotes = True,
            keep_pre = True
        )
    try:
        if outfile is not None:
            with open('www/blog/' + outfile, 'w') as fh:
                fh.write(html)
    except OSError:
        pass
    except IOError:
        pass

    return html

@error(404)
def error404(error):
    """Display the error 404 page"""
    return server_static('error/404.html')

@get('/')
@get('/blog/index.html')
def index():
    """Display the homepage"""
    #return static_file('index.html', root='www')
    data = {'body_title': '¡Hola!',
            'head_title': 'Vijay Mahrra: ¡Hola!',
            'head_author': 'Vijay Mahrra',
            'head_keywords': 'Blog',
            'head_description': 'Blog',
            'blog_posts_meta': get_blog_posts_meta()}
    return generate_page(data = data, tpl = 'home.tpl', outfile = 'index.html')
    #return static_file('index.html', root='www')

@get('/blog/<url>')
def blog(url):
    """Display the blog post"""
    filename = url[0:-5] + '.md'
    return blog_markdown_to_html(filename)

def blog_markdown_to_html(filename):
    """Generate a blog post html page from a supplied markdown filename"""
    document = str()
    documents = get_files_by_ext('.md', 'content')
    if filename in documents:
        filepath = documents[filename]
        html, meta, document = parse_markdown_file(filepath)
        data = {
            'body_title': "".join(meta['title']),
            'head_title': 'Vijay Mahrra: ' + "".join(meta['title']),
            'head_author': 'Vijay Mahrra',
            'head_keywords': meta['tags'],
            'head_description': "".join(meta['title']),
            'body_content': html,
            'meta': meta,
            'date': meta['date']
        }
        return generate_page(tpl = 'blog_post', data = data, outfile = filename[0:-3] + '.html')


@get('/js/<filepath:path>')
def js(filepath):
    """Return minified/compressed js"""
    try:
        path = 'www/js/' + filepath
        with open(path) as fh:
            minified = jsmin(fh.read(), quote_chars="'\"`")
            return minified
    except IOError:
        return static_file(filepath, root='www')

@get('/<filepath:path>')
def server_static(filepath):
    """Display static files in the web root folder"""
    return static_file(filepath, root='www')

application=default_app()

if __name__ in ('__main__'):
    cache_clear()
#    generate_static_website()
    from waitress import serve
    run(server='waitress')
