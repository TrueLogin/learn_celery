"""This class/processor compiles a PDF document from separate pages"""

import os

from fnmatch import fnmatch
from PyPDF2 import PdfFileReader, PdfFileWriter

class CompilePdfProcessor: # pylint: disable=too-few-public-methods
    """This class/processor compiles a PDF document from separate pages"""

    WATERMARKED_PDF_PATTERN = '*_watermarked.pdf'

    def __init__(self, tmp_dir_path, original_filepath) -> None:
        self.tmp_dir_path = tmp_dir_path
        self.original_filepath = original_filepath

    def call(self) -> str:
        """Runs the process"""
        compiled_pdf_path = self.__compiled_pdf_path()

        with open(compiled_pdf_path, 'wb') as compiled_output:
            pdf_compiler = PdfFileWriter()

            for page in sorted(self.__watermarked_pages()):
                watermarked_page = PdfFileReader(page).getPage(0)
                pdf_compiler.addPage(watermarked_page)

            pdf_compiler.write(compiled_output)

        return compiled_pdf_path

    def __compiled_pdf_path(self) -> str:
        """Get the full path to the final pdf"""
        original_name_with_ext = os.path.basename(self.original_filepath)
        original_basename = os.path.splitext(original_name_with_ext)[0]
        watermarked_basename = f'{original_basename}_watermarked.pdf'

        return os.path.join(self.__original_dir(), watermarked_basename)

    def __original_dir(self) -> str:
        """Get the dir of the original pdf file"""
        return os.path.dirname(self.original_filepath)

    def __watermarked_pages(self) -> list:
        """Get the list of watermarked pages in tmp"""
        return [
            os.path.join(self.tmp_dir_path, name)
            for name in os.listdir(self.tmp_dir_path)
            if os.path.isfile(name)
            if fnmatch(name, self.WATERMARKED_PDF_PATTERN)
        ]
