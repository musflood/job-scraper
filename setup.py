from setuptools import setup

setup(
    name='job-scraper',
    description='Scrapes the first ten pages of StackOverflow Jobs for Python jobs',
    package_dir={'': 'src'},
    py_modules=[
        'scraper'
    ],
    authors='Megan Flood',
    author_email='mak.flood@comcast.net',
    install_requires=[
        'requests',
        'beautifulsoup4'
    ]
)
