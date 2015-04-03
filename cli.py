# -*- coding: utf-8 -*-
'''
Beautifully Simple Static Bottle Blog Generator
===============================================

Command Line Interface using Click http://click.pocoo.org/
'''
import click

if __name__ == '__main__':
    pass

    data = {'body_title': CONFIG['title'] + ' / ' + filename[:-5],
            'head_title': filename[:-5],
            'head_author': CONFIG['author'],
            'head_keywords': filename[:-5] + ' file',
            'head_description': filename[:-5 + ' for website ' + CONFIG['title'],
            'blog_posts_meta': get_blog_posts_meta(),
            'body_content': parse_markdown_file('docs/' + filename[:-3])}

