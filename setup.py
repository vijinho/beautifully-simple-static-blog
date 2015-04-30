try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Beautifully Simple Static Blog',
    'author': 'Vijay Mahrra',
    'author_email': 'vijay.mahrra@gmail.com',
    'maintainer': 'Vijay Mahrra',
    'maintainer_email': 'vijay.mahrra@gmail.com',
    'contact': 'Vijay Mahrra',
    'contact_email': 'vijay.mahrra@gmail.com',
    'url': 'https://github.com/vijinho/beautifully-simple-static-blog',
    'download_url': 'https://github.com/vijinho/beautifully-simple-static-blog',
    'version': '1.0',
    'keywords': ['static blog','bottle blog','static website generator','bottle','static website'],
    'install_requires': ['waitress', 'htmlmin', 'jsmin', 'csscompressor', 'future', 'bottle', 'markdown', 'click'],
    'packages': ['besistblog'],
    'scripts': [],
    'name': 'besistblog'
}

setup(**config)
