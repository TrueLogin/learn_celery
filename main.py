"""Just a starting point"""

import os

from .processors import SplitPdfProcessor, PdfPageProcessor, CompilePdfProcessor

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
    print('- Processing finished')
    print(f'- {watermarked_pages}')

    print('- Compile the document back')
    processor = CompilePdfProcessor(tmp_dir_path, original_document)
    compiled_pdf_path = processor.call()
    print('- Compiled')
    print(f'Processing completed: {compiled_pdf_path}')

    remove_tmp_files(tmp_dir_path)

def remove_tmp_files(dir_path):
    """Removes tmp files from .tmp directory"""
    if dir_path == os.getcwd():
        os.chdir('..')

    for filename in os.listdir(dir_path):
        file = os.path.join(dir_path, filename)
        os.remove(file)

    os.rmdir(dir_path)
