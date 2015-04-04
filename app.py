# -*- coding: utf8 -*-
"""
Website Application - Runs webserver for markdown files and generates
static content.
"""
import os
import sys
import pickle
import hashlib
import time
import shutil

import htmlmin
from jsmin import jsmin
import markdown
from bottle import error, get, static_file, template, default_app, run

import email.Utils
from fnmatch import fnmatch

__author__ = "Vijay Mahrra"
__copyright__ = "Copyright 2015, Vijay Mahrra"
__credits__ = ["Vijay Mahrra"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Vijay Mahrra"
__email__ = "vijay.mahrra@gmail.com"
__status__ = "Production"

reload(sys)
sys.setdefaultencoding('utf8')

if not os.path.exists('config.py'):
    shutil.copyfile('config.py.example', 'config.py')
from config import CONFIG


class MyUtils:
    """General utility helper functions used by the app"""

    def __init__(self):
        pass

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

    @staticmethod
    def hashed(key):
        """Generate a string hash from a given key string"""
        return hashlib.sha1(key).hexdigest()


class ObjectCache:
    """Handle caching for objects using picklet"""
    directory = None
    fileformat = None

    def __init__(self, directory = None, fileformat = None):
        """"directory is where cache files are stored
        and naming format for the cache files
        """
        self.directory = directory
        if fileformat is None:
            self.fileformat = "{dir}/{key}.tmp"
        else:
            self.fileformat = fileformat

    def set(self, key, data):
        """Save an item of data to the cache - return boolean success"""
        if CONFIG['cache'] is False:
            return False
        try:
            filename = self.fileformat.format(dir=self.directory,
                                               key=Utils.hashed(key))
            pickle.dump(data, open(filename, "wb"))
            return True
        except IOError:
            return False

    def get(self, key):
        """Get an item of data from the cache - return data or empty dict"""
        try:
            filename = self.fileformat.format(dir=self.directory,
                                               key=Utils.hashed(key))
            data = pickle.load(open(filename, "rb"))
            return data
        except IOError:
            return {}

    def rm(self, key):
        """Remove an item of data from the cache - return boolean success"""
        try:
            filename = self.fileformat.format(dir=self.directory,
                                               key=Utils.hashed(key))
            os.remove(filename)
            return True
        except OSError:
            return False
        except IOError:
            return False

    def wipe(self):
        """Wipe the cache - return removed files list"""
        try:
            files = Files.by_extension('tmp', self.directory, cache=False)
            removed = [os.remove(path) for filename, path in files.iteritems()]
        except OSError:
            return []
        except IOError:
            return []
        return removed


class MyMarkdown:
    """My Markdown Utility"""
    output_format = None
    extensions = None

    def __init__(self, output_format = None, extensions = []):
        """set the default output format and extensions to use"""
        if output_format is None:
            self.output_format = 'html5'
        else:
            self.output_format = output_format

        if len(extensions) is 0:
            self.extensions = ['markdown.extensions.meta']
        else:
            self.extensions = extensions

    def parse(self, text):
        """Return text contents as (str html5, dict meta-information,
        str original markdown)
        """
        md = markdown.Markdown(output_format=self.output_format,
                               extensions=self.extensions)
        html = md.convert(text)
        meta = {}
        if len(md.Meta) > 0:
            for k, v in md.Meta.iteritems():
                v = "".join(v)
                if k == 'tags' and len(v) > 2:
                    v = v[1:-1]
                meta[k] = v
        return html, meta, text

    @staticmethod
    def file(path):
        """Read a file name and return contents as str html5,
        dict meta-information, original markdown
        """
        with open(path) as fh:
            return Markdown.parse(fh.read())


class MyFiles:
    """File handling methods"""
    def __init__(self):
        pass

    @staticmethod
    def by_extension(ext, path, cache=None):
        """Return a dict of all files of a given file extension"""
        if cache is None:
            cache = CONFIG['cache']
        cache_key = ext + path
        matches = Cache.get(cache_key)
        if cache is False or matches is False or len(matches) is 0:
            matches = {}
            ext = '*.' + ext
            for root, dirs, files in os.walk(path):
                for f in files:
                    if fnmatch(f, ext):
                        matches[f] = str(os.path.join(root, f))
            Cache.set(cache_key, matches)
        return matches


class MyBlog:
    def __init__(self):
        pass

    @staticmethod
    def metadata(cache=None):
        """Return a dict of meta-information for all blog posts"""
        if cache is None:
            cache = CONFIG['cache']
        cache_key = 'blog_posts_meta'
        data = Cache.get(cache_key)
        if cache is False or data is False or len(data) is 0:
            documents = Files.by_extension('md', CONFIG['content_dir'])
            for filename, filepath in documents.items():
                filepath = documents[filename]
                html, meta, document = Markdown.file(filepath)
                # add some extra information we might find useful
                meta['id'] = Utils.hashed(filepath)
                meta['rfc822date'] = Utils.ts_to_rfc822(meta['date'])
                meta['filename'] = filename
                meta['filepath'] = filepath
                data[filename] = meta
                Cache.set(cache_key, data)
        return data

    @staticmethod
    def generate():
        """Generate static www/blog/*.html files from content/*.md files"""
        data = {}
        documents = Files.by_extension('md', CONFIG['content_dir'])
        for filename, filepath in documents.items():
            filepath = documents[filename]
            html, meta, document = Markdown.file(filepath)
            meta['filename'] = filename
            meta['filepath'] = filepath
            data[filename] = meta
            Blog.html(filename)
        return data

    @staticmethod
    def html(filename):
        """Generate a blog post html page from a supplied markdown filename"""
        documents = Files.by_extension('md', CONFIG['content_dir'])
        if filename in documents:
            filepath = documents[filename]
            html, meta, document = Markdown.file(filepath)
            data = {
                'body_title': "".join(meta['title']),
                'head_title': CONFIG['author'] + ": " + "".join(meta['title']),
                'head_author': CONFIG['author'],
                'head_keywords': meta['tags'],
                'head_description': "".join(meta['title']),
                'body_content': html,
                'meta': meta,
                'date': meta['date']
            }
            if CONFIG['generate'] is False:
                return Generate.page(tpl='blog_post', data=data)
            else:
                return Generate.page(tpl='blog_post', data=data,
                                     outfile=filename[0:-3] + '.html')


class MyGenerate:
    """Output file rendering and website generation"""
    def __init__(self):
        pass

    @staticmethod
    def page(data=None,
             header='header.tpl',
             tpl='default',
             footer='footer.tpl',
             minify=None,
             outfile=None):
        """Combine multiple (header, body, footer) templates injecting dict data
        and return generated output
        """
        if minify is None:
            minify = CONFIG['minify_html']
        html = template(header, data=data, cfg=CONFIG) + \
            template(tpl, data=data, cfg=CONFIG) + \
            template(footer, data=data, cfg=CONFIG)
        if minify is True:
            html = htmlmin.minify(html,
                                  remove_comments=True,
                                  remove_all_empty_space=True,
                                  reduce_empty_attributes=True,
                                  reduce_boolean_attributes=True,
                                  remove_optional_attribute_quotes=True,
                                  keep_pre=True)
        try:
            if outfile is not None:
                with open(CONFIG['blog_dir'] + outfile, 'w') as fh:
                    fh.write(html)
        except OSError:
            pass
        except IOError:
            pass

        return html

    @staticmethod
    def feed(data=None, tpl='rss.tpl', outfile='rss.xml'):
        """Render a multiple templates using the same data dict for header,
        body, footer templates
        """
        xml = template(tpl,
                       data=data,
                       cfg=CONFIG,
                       date=email.Utils.formatdate(),
                       author=CONFIG['email'] + '(' + CONFIG['author'] + ')')
        try:
            if outfile is not None:
                with open(CONFIG['blog_dir'] + outfile, 'w') as fh:
                    fh.write(xml)
        except OSError:
            pass
        except IOError:
            pass

        return xml

    @staticmethod
    def website():
        """Generate the static website files"""
        try:
            files = Files.by_extension('md', CONFIG['docs_dir'], cache=False)
            for filename, filepath in files.iteritems():
                docs(filename[:-3] + '.html')
        except OSError:
            pass
        except IOError:
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
            'blog_posts_meta': Blog.metadata()}
    return Generate.page(data=data, tpl='home.tpl', outfile='index.html')


@get('/blog/<url>')
def blog(url):
    """Display the blog post"""
    filename = url[:-5] + '.md'
    return Blog.html(filename)


@get('/blog/docs/<filename>')
def docs(filename):
    """Display the docs folder files"""
    html, meta, text = Markdown.file('docs/' + filename[:-5] + '.md')
    data = {'head_title': filename[:-5],
            'head_author': CONFIG['author'],
            'head_keywords': filename[:-5] + ' file',
            'head_description': filename[:-5] + ' for website ' + CONFIG[
                'title'],
            'blog_posts_meta': Blog.metadata(),
            'body_content': html}
    return Generate.page(data=data, tpl='default.tpl',
                         outfile='docs/' + filename)


@get('/rss')
@get('/rss.xml')
@get('/blog/rss')
@get('/blog/rss.xml')
@get('/sitemap.xml')
def rss():
    """Display the homepage"""
    data = {'body_title': CONFIG['title'],
            'head_title': CONFIG['author'] + ': ¡Hola!',
            'head_author': CONFIG['author'],
            'head_keywords': 'Blog',
            'head_description': 'Blog',
            'blog_posts_meta': Blog.metadata()}
    return Generate.feed(data=data)


@get('/js/<filepath:path>')
def js(filepath):
    """Return minified/compressed js"""
    if CONFIG['minify_js'] is False:
        return static_file(filepath, root=CONFIG['web_dir'])
    else:
        try:
            path = CONFIG['js_dir'] + filepath
            with open(path) as fh:
                minified = jsmin(fh.read(), quote_chars="'\"`")
                return minified
        except IOError:
            return static_file(filepath, root=CONFIG['web_dir'])


@get('/<filepath:path>')
def server_static(filepath):
    """Display static files in the web root folder"""
    return static_file(filepath, root=CONFIG['web_dir'])


application = default_app()

if __name__ in '__main__':
    Utils = MyUtils()
    Cache = ObjectCache(CONFIG['cache_dir'])
    Markdown = MyMarkdown('html5', ['markdown.extensions.meta'])
    Files = MyFiles()
    Blog = MyBlog()
    Generate = MyGenerate()

    print "Clearing cache dir " + CONFIG['blog_dir'] + "..."
    Cache.wipe()

    if CONFIG['debug'] is True:
        CONFIG['cache'] = False
        CONFIG['generate'] = False
        CONFIG['minify_js'] = False
        CONFIG['minify_html'] = False

    if CONFIG['generate'] is True:
        print "Generating static files in " + CONFIG['blog_dir'] + " ..."
        Generate.website()

    run(server='waitress')
