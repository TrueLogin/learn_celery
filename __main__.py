"""
Package created to learn Celery
"""

import sys

def main(argv):
    """
        The function runs the pdf file processing.
        It takes file name and passes to first Celery worker

        The whole proccess looks like:

        - Enqueue Celery worker to find and brake file to pages
        - Update each page as a Celery task (in parallel)
        - Compile a single file back from updated pages
    """
    print(f'argv[1] = {argv[1]}')

main(sys.argv)
