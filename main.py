"""Just a starting point"""

import os

from .processors import SplitPdfProcessor, PdfPageProcessor

def main(argv) -> None:
    """
        The function runs the pdf file processing.
        It takes file name and passes to first Celery worker

        The whole proccess looks like:

        - Enqueue Celery worker to find and brake file to pages
        - Update each page as a Celery task (in parallel)
        - Compile a single file back from updated pages
    """
    original_document = argv[1]
    watermark_document = argv[2]
    print(f'Process document: {original_document}')
    print('- Split document')
    split_processor = SplitPdfProcessor(original_document)
    tmp_dir_path = split_processor.call()
    print(f'- Pages are saved here: {tmp_dir_path}')
    print('- Process pages')
    pages = [
        os.path.join(tmp_dir_path, name)
        for name in os.listdir(tmp_dir_path)
        if os.path.isfile(name)
    ]
    watermarked_pages = []
    for page in pages:
        page_processor = PdfPageProcessor(page, watermark_document)
        watermarked_pages.append(page_processor.call())
