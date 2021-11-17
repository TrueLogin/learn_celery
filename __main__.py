"""Package created to learn Celery"""

import sys
from .src.processors import split_pdf_processor

def main(argv) -> None:
    """
        The function runs the pdf file processing.
        It takes file name and passes to first Celery worker

        The whole proccess looks like:

        - Enqueue Celery worker to find and brake file to pages
        - Update each page as a Celery task (in parallel)
        - Compile a single file back from updated pages
    """
    print(f'argv[1] = {argv[1]}')
    split_processor = split_pdf_processor.SplitPdfProcessor(argv[1])
    tmp_dir_path = split_processor.call()
    print(f'Pages are saved here: {tmp_dir_path}')

main(sys.argv)
