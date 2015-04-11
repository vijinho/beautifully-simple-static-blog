# -*- coding: utf8 -*-
"""
Website Application - Runs webserver for markdown files and generates
static content.
"""
from builtins import str
from builtins import object
import os
import pickle
import hashlib
import time
import shutil
from fnmatch import fnmatch
import re
import codecs
import htmlmin
from jsmin import jsmin
import csscompressor
import markdown
from bottle import error, get, static_file, response, template, default_app, run

import email


__author__ = "Vijay Mahrra"
__copyright__ = "Copyright 2015, Vijay Mahrra"
__credits__ = ["Vijay Mahrra"]
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Vijay Mahrra"
__email__ = "vijay.mahrra@gmail.com"
__status__ = "Production"


def hashed(key):
    """Generate a string hash from a given key string"""
    return hashlib.sha1(key.encode('utf-8')).hexdigest()


def files_by_extension(ext, path):
    """Generator (filename,filepath) for a given file extension
    in a directory tree
    """
    ext = '*.' + ext
    for root, dirs, files in os.walk(path):
        for f in files:
            if fnmatch(f, ext):
               yield f, str(os.path.join(root, f))


def files_by_ext(ext, path, cache=False):
    """Return a dict of all files of a given file extension, using caching"""
    cache_key = ext + path
    if cache:
        matches = Cache.get(cache_key)
    else:
        matches = None
    if not (cache or matches):
        matches = {}
        for file, filepath in files_by_extension(ext, path):
            matches[file] = filepath
        Cache.set(cache_key, matches)
    return matches


class ObjectCache(object):
    """Handle caching for objects using picklet"""

    def __init__(self,
                 cfg=None,
                 directory=None,
                 fileformat="{dir}/{key}.tmp"):
        """"directory is where cache files are stored
        and naming format for the cache files
        """
        self.config = cfg
        self.fileformat = fileformat
        if directory:
            self.directory = directory
        else:
            self.directory = cfg['cache_dir']

    def set(self, key, data):
        """Save an item of data to the cache - return boolean success"""
        if self.config['cache'] is False:
            return False
        try:
            filename = self.fileformat.format(dir=self.directory,
                                              key=hashed(key))
            pickle.dump(data, open(filename, "wb"))
            return True
        except IOError:
            return False

    def get(self, key):
        """Get an item of data from the cache - return data or empty dict"""
        try:
            filename = self.fileformat.format(dir=self.directory,
                                              key=hashed(key))
            data = pickle.load(open(filename, "rb"))
            return data
        except IOError:
            return {}

    def rm(self, key):
        """Remove an item of data from the cache - return boolean success"""
        try:
            filename = self.fileformat.format(dir=self.directory,
                                              key=hashed(key))
            os.remove(filename)
            return True
        except (OSError, IOError):
            return False

    def wipe(self):
        """Wipe the cache return boolean success"""
        try:
            for file, filepath in files_by_extension('tmp', self.directory):
                os.remove(filepath)
        except (OSError, IOError):
            return False
        return True


class MyMarkdown(object):
    """My Markdown Utility"""

    def __init__(self, output_format='html5', extensions=None):
        """set the default output format and extensions to use"""
        if not extensions:
            extensions = ['markdown.extensions.meta']
        self.output_format = output_format
        self.extensions = extensions

    def parse(self, text):
        """Return text contents as (str html5, dict meta-information,
        str original markdown)
        """
        md = markdown.Markdown(output_format=self.output_format,
                               extensions=self.extensions)
        html = md.convert(text)
        meta = {}
        for k, v in md.Meta.items():
            v = "".join(v)
            # the tags in the markdown file are stored as [tag1, tag,2...]
            # so clip the [ and the ] from the string
            if k == 'tags' and len(v) > 2:
                v = v[1:-1]
            meta[k] = v
        return html, meta, text

    @staticmethod
    def file(path):
        """Read a file name and return contents as str html5,
        dict meta-information, original markdown
        """
        with codecs.open(path, 'r', 'utf8')  as fh:
            return Markdown.parse(fh.read())


class MyBlog(object):
    def __init__(self, cfg=None, directory=None):
        self.config = cfg
        if directory:
            self.directory = directory
        else:
            self.directory = cfg['content_dir']

    @staticmethod
    def ts_to_rfc822(timestamp=None, timezone='GMT'):
        """Convert datetime from (mysql-style) timestamp format
        1976-12-25 07:30:30 to RFC822 string
        """
        l = len(timestamp)
        if l == 19:
            fmt = '%Y-%m-%d %H:%M:%S'
        elif l == 16:
            fmt = '%Y-%m-%d %H:%M'
        elif l == 10:
            fmt = '%Y-%m-%d'
        elif l == 8:
            fmt = '%y-%m-%d'
        else:
            return ''

        return time.strftime("%a, %d %b %Y %H:%M:%S " + timezone,
                             time.strptime(timestamp, fmt))

    def metadata(self, cache=False):
        """Return a dict of meta-information for all blog posts"""
        cache_key = 'blog_posts_meta'
        data = Cache.get(cache_key)
        if cache is False or data is False or len(data) is 0:
            documents = files_by_ext('md', self.directory, cache)
            for filename, filepath in documents.items():
                filepath = documents[filename]
                html, meta, document = Markdown.file(filepath)
                # add some extra information we might find useful
                meta['id'] = hashed(filepath)
                meta['rfc822date'] = self.ts_to_rfc822(meta['date'])
                meta['filename'] = filename
                meta['filepath'] = filepath
                data[filename] = meta
            Cache.set(cache_key, data)
        return data

    def generate(self):
        """Generate static www/blog/*.html files from content/*.md files"""
        data = {}
        documents = files_by_ext('md', self.directory)
        for filename, filepath in documents.items():
            filepath = documents[filename]
            html, meta, document = Markdown.file(filepath)
            meta['filename'] = filename
            meta['filepath'] = filepath
            data[filename] = meta
            Blog.html(filename)
        return data

    def html(self, filename, cfg=None):
        """Generate a blog post html page from a supplied markdown filename
        default config values used if no config specified
        """
        if cfg is None:
            cfg = self.config

        documents = files_by_ext('md', self.directory)
        if filename in documents:
            filepath = documents[filename]
            html, meta, document = Markdown.file(filepath)
            data = {
                'body_title': "".join(meta['title']),
                'head_title': cfg['author'] + ": " + "".join(
                    meta['title']),
                'head_author': cfg['author'],
                'head_keywords': meta['tags'],
                'head_description': "".join(meta['title']),
                'body_content': html,
                'meta': meta,
                'date': meta['date']
            }
            if cfg['generate'] is False:
                return Generate.page(tpl='blog_post', data=data)
            else:
                return Generate.page(tpl='blog_post', data=data,
                                     outfile=filename[0:-3] + '.html')


class MyGenerate(object):
    """Output file rendering and website generation"""

    def __init__(self, cfg=None, directory=None, docs_directory=None):
        self.config = cfg

        if directory:
            self.directory = directory
        else:
            self.directory = cfg['output_dir']

        if docs_directory:
            self.docs_directory = docs_directory
        else:
            self.docs_directory = cfg['docs_dir']

    @staticmethod
    def minify_html(html):
        """Return minified HTML"""
        if html is None:
            return ''
        return htmlmin.minify(html,
                              remove_comments=True,
                              remove_all_empty_space=True,
                              reduce_empty_attributes=True,
                              reduce_boolean_attributes=True,
                              remove_optional_attribute_quotes=True,
                              keep_pre=True)

    def css(self, path):
        """Return optionally minified CSS for filepath"""
        if self.config['minify_css'] is False:
            with codecs.open(path, 'r', 'utf8')  as fh:
                data = fh.read()
        else:
            with codecs.open(path, 'r', 'utf8')  as fh:
                data = csscompressor.compress(fh.read())

        try:
            if self.config['generate'] is True and len(data) > 0:
                outfile = self.config['css_output'] + '/' + os.path.basename(
                    path)
                with open(outfile, 'wb') as fh:
                    fh.write(str(data).encode('utf8'))
        except (OSError, IOError):
            pass
        return data

    def inline_css(self, stylesheets=None, cfg=None):
        """Return concatenated css ready to insert into html document"""
        if stylesheets is None:
            return ''
        if cfg is None:
            cfg = self.config
        html = "\n<!-- Inline CSS -->\n<style>\n"
        for stylesheet in stylesheets:
            html = "\n" + html + self.css(
                cfg['css_dir'] + '/' + stylesheet)
        html += "\n</style>\n<!-- End Inline CSS -->\n"
        return html

    def js(self, path):
        """Return optionally minified JS for filepath"""
        if self.config['minify_js'] is False:
            with open(path) as fh:
                data = fh.read()
        else:
            with codecs.open(path, 'r', 'utf8')  as fh:
                data = jsmin(fh.read(), quote_chars="'\"`")
        try:
            if self.config['generate'] is True and len(data) > 0:
                outfile = self.config['js_output'] + '/' + os.path.basename(
                    path)
                with open(outfile, 'wb') as fh:
                    fh.write(str(data).encode('utf8'))
        except (OSError, IOError):
            pass
        return data

    def inline_js(self, scripts, cfg=None):
        """Return concatenated js ready to insert into html document"""
        if scripts is None:
            return ''
        if cfg is None:
            cfg = self.config
        html = "\n<!-- Inline Javascript -->\n<script type=\"text/javascript\">\n/* <![CDATA[ */\n"
        for script in scripts:
            html = "\n" + html + self.js(
                cfg['js_dir'] + '/' + script)
        html += "\n/* ]]> */\n</script>\n<!-- End Inline Javascript -->\n"
        return html

    def page(self,
             data=None,
             header='header.tpl',
             tpl='default',
             footer='footer.tpl',
             minify=None,
             outfile=None,
             cfg=None):
        """Combine multiple (header, body, footer) templates injecting dict data
        and return generated output
        """
        if cfg is None:
            cfg = self.config

        if minify is None:
            minify = cfg['minify_html']

        styles = ''
        if len(cfg['css_inline']) > 0:
            cache_key = 'inline-styles'
            if self.config['cache'] is True:
                styles = Cache.get(cache_key)
            if len(styles) is 0 or styles is False:
                styles = self.inline_css(cfg['css_inline'], cfg)
                Cache.set(cache_key, styles)
        data['css'] = styles

        source = ''
        if len(cfg['js_inline']) > 0:
            cache_key = 'inline-js'
            if self.config['cache'] is True:
                source = Cache.get(cache_key)
            if len(source) is 0 or source is False:
                source = self.inline_js(cfg['js_inline'], cfg)
                Cache.set(cache_key, styles)
        data['js'] = source

        html = template(header, data=data, cfg=cfg) + \
               template(tpl, data=data, cfg=cfg) + \
               template(footer, data=data, cfg=cfg)

        if minify is True:
            html = self.minify_html(html)
        try:
            if outfile is not None and cfg['generate'] is True:
                with open(self.directory + '/' + outfile, 'wb') as fh:
                    fh.write(str(html).encode('utf8'))
        except OSError:
            pass
        except IOError:
            pass
        return html

    def feed(self, data=None, feedtype='rss', tpl='rss.tpl', outfile='rss.xml',
             cfg=None):
        """Render a multiple templates using the same data dict for header,
        body, footer templates
        """
        if cfg is None:
            cfg = self.config

        xml = None
        if feedtype is 'rss':
            xml = template(tpl,
                           data=data,
                           cfg=cfg,
                           date=email.utils.formatdate(),
                           author=cfg['email'] + '(' + cfg[
                               'author'] + ')')
        try:
            if outfile is not None and xml is not None:
                with open(self.directory + '/' + outfile, 'wb') as fh:
                    fh.write(str(xml).encode('utf8'))
        except (OSError, IOError):
            pass

        return xml

    def website(self):
        """Generate the static website files"""
        try:
            files = files_by_ext('md', self.docs_directory,
                                              cache=False)
            for filename, filepath in files.items():
                docs(filename[:-3] + '.html')
        except (OSError, IOError):
            pass
        Blog.generate()
        rss()
        index()


@error(404)
def error404():
    """Display the error 404 page"""
    return server_static('error/404.html')


@get('/')
@get('/blog/index.html')
def index():
    """Display the homepage"""
    data = {'body_title': CONFIG['title'],
            'head_title': CONFIG['author'] + ': ¡Hola!',
            'head_author': CONFIG['author'],
            'head_keywords': 'Blog',
            'head_description': 'Blog',
            'blog_posts_meta': Blog.metadata(cache=True)}
    return Generate.page(data=data, tpl='home.tpl', outfile='index.html')


@get('/blog/<url>')
def blog(url):
    """Display the blog post"""
    m = re.match('^[\d]+[\d]+[\d]+.*\.html', url)
    if hasattr(m, 'group'):
        filename = url[:-5] + '.md'
        return Blog.html(filename)
    else:
        m = re.match('^[^\.]+\.html', url)
        if hasattr(m, 'group'):
            return docs(url)
        return error404()


@get('/blog/docs/<filename>')
def docs(filename):
    """Display the docs folder files"""
    m = re.match('^[^\.]+\.html', filename)
    if not hasattr(m, 'group'):
        return error404()
    html, meta, text = Markdown.file('docs/' + filename[:-5] + '.md')
    data = {'head_title': filename[:-5],
            'head_author': CONFIG['author'],
            'head_keywords': filename[:-5] + ' file',
            'head_description': filename[:-5] + ' for website ' + CONFIG[
                'title'],
            'blog_posts_meta': Blog.metadata(cache=True),
            'body_content': html}
    return Generate.page(data=data,
                         tpl='default.tpl',
                         outfile=filename)


@get('/rss')
@get('/rss.xml')
@get('/blog/rss')
@get('/blog/rss.xml')
@get('/sitemap.xml')
def rss():
    """Display the homepage"""
    response.content_type = 'application/rss+xml; charset=utf8'
    data = {'body_title': CONFIG['title'],
            'head_title': CONFIG['author'] + ': ¡Hola!',
            'head_author': CONFIG['author'],
            'head_keywords': 'Blog',
            'head_description': 'Blog',
            'blog_posts_meta': Blog.metadata(cache=True)}
    return Generate.feed(data=data)


@get('/blog/js/<filepath:path>')
def js(filepath):
    """Return minified/compressed js"""
    m = re.match('^[^\.]+\.js', filepath)
    if hasattr(m, 'group'):
        response.content_type = 'application/javascript; charset=utf8'
        path = CONFIG['js_dir'] + '/' + filepath
        try:
            return Generate.js(path)
        except IOError:
            with codecs.open(path, 'r', 'utf8')  as fh:
                return fh.read()
    else:
        return error404()


@get('/blog/css/<filepath:path>')
def css(filepath):
    """Return minified/compressed css"""
    m = re.match('^[^\.]+\.css', filepath)
    if hasattr(m, 'group'):
        response.content_type = 'text/css; charset=utf8'
        path = CONFIG['css_dir'] + '/' + filepath
        try:
            return Generate.css(path)
        except IOError:
            with codecs.open(path, 'r', 'utf8')  as fh:
                return fh.read()
    else:
        return error404()


@get('/<filepath:path>')
def server_static(filepath):
    """Display static files in the web root folder"""
    return static_file(filepath, root=CONFIG['www_root'])


application = default_app()

if __name__ in '__main__':

    if not os.path.exists('config.py'):
        shutil.copyfile('config.py.example', 'config.py')
    import config

    CONFIG = config.Config().get()

    Markdown = MyMarkdown()
    Blog = MyBlog(cfg=CONFIG)
    Cache = ObjectCache(cfg=CONFIG)
    Generate = MyGenerate(cfg=CONFIG)
    if CONFIG['generate'] is True:
        Cache.wipe()
        Generate.website()

    run(server='waitress')
