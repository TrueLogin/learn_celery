"""Setup"""

from setuptools import setup

setup(
    name='LearnCelery',
    url='https://github.com/TrueLogin/learn_celery',
    author='TrueLogin',
    author_email='',
    packages=['processors'],
    install_requires=['celery', 'redis', 'PyPDF2', 'rabbitmq'],
    version='0.1'
)
