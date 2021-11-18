"""Just a starting point"""

import sys
import processors

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
    split_processor = processors.SplitPdfProcessor(argv[1])
    tmp_dir_path = split_processor.call()
    print(f'Pages are saved here: {tmp_dir_path}')

if __name__ == '__main__':
    main(sys.argv)
