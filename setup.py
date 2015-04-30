try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'besistblog',
    'description': "Beautifully Simple Static Blog Generator is a static blog generator.",
    'keywords': ['static blog','bottle blog','static website generator','bottle','static website'],
    'url': 'https://github.com/vijinho/beautifully-simple-static-blog',
    'download_url': 'https://github.com/vijinho/beautifully-simple-static-blog',
    'version': '1.0',
    'license': 'GPLv3',
    'classifiers': [
        "Framework :: Bottle",
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development'
    ],
    'install_requires': [i.strip() for i in open("requirements.txt").readlines()],
    'packages': ['besistblog'],
    'scripts': [],
    'entry_points': {
        'console_scripts': []
    },
    'author': 'Vijay Mahrra',
    'author_email': 'vijay.mahrra@gmail.com',
    'maintainer': 'Vijay Mahrra',
    'maintainer_email': 'vijay.mahrra@gmail.com',
    'contact': 'Vijay Mahrra',
    'contact_email': 'vijay.mahrra@gmail.com'
}

setup(**config)
