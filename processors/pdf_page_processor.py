"""This class/processor works with a single page"""

import os

from PyPDF2 import PdfFileReader, PdfFileWriter

class PdfPageProcessor: # pylint: disable=too-few-public-methods
    """This class/processor works with a single page"""

    def __init__(self, page_filepath, watermark_filepath) -> None:
        self.page_filepath = page_filepath
        self.watermark_filepath = watermark_filepath

    def call(self) -> str:
        """Runs the process"""
        source_page = PdfFileReader(self.page_filepath).getPage(0)
        watermark_page = PdfFileReader(self.watermark_filepath).getPage(0)
        watermarked_pdf_writer = PdfFileWriter()

        source_page.mergePage(watermark_page)
        watermarked_pdf_writer.addPage(source_page)

        watermarked_page_filepath = self.__watermarked_page_filepath()
        with open(watermarked_page_filepath, 'wb') as outcoming_pdf:
            watermarked_pdf_writer.write(outcoming_pdf)

        return watermarked_page_filepath

    def __watermarked_page_filepath(self) -> str:
        """Generate file path for watermarked page"""
        original_with_ext = os.path.basename(self.page_filepath)
        original_name = os.path.splitext(original_with_ext)[0]
        watermarked_name = f'{original_name}_watermarked.pdf'

        relative_script_path = os.path.abspath(self.page_filepath)
        tmp_dir_path = os.path.dirname(relative_script_path)
        tmp_dir_path = tmp_dir_path.split('/')
        tmp_dir_path.append(watermarked_name)

        return '/'.join(tmp_dir_path)
