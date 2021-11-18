"""This class/processor saves each page as a separate pdf doc"""

import os

from PyPDF2 import PdfFileReader, PdfFileWriter

class SplitPdfProcessor: # pylint: disable=too-few-public-methods
    """This class/processor saves each page as a separate pdf doc"""

    def __init__(self, original_pdf_filepath) -> None:
        self.original_pdf_filepath = original_pdf_filepath

    def call(self) -> str:
        """Starts splitting a document"""

        print(f'Path to original file: {self.original_pdf_filepath}')
        tmp_dir_path = self.__create_tmp_dir()
        self.__split_document(tmp_dir_path)
        return tmp_dir_path

    def __pdf_filename(self) -> str:
        """Returns pdf's file name without extension"""
        filename_with_ext = os.path.basename(self.original_pdf_filepath)
        return os.path.splitext(filename_with_ext)[0]

    def __create_tmp_dir(self) -> str:
        """
            Creates a temp dir to save all the pages.\n
            It changes working directory
        """
        tmp_dir_name = self.__pdf_filename()

        relative_script_path = os.path.abspath(__file__)
        script_dir_name = os.path.dirname(relative_script_path)
        root_app_dir = script_dir_name.split('/')[0:-1]

        # add tmp dir to the list for further join
        root_app_dir.append('tmp')
        tmp_dir_path = '/'.join(root_app_dir)
        os.chdir(tmp_dir_path)

        if not os.path.exists(tmp_dir_name):
            os.mkdir(tmp_dir_name)
            print(f'-- Directory created successfully ({tmp_dir_name})')
        else:
            print(f'-- Directory exists ({tmp_dir_name})')

        root_app_dir.append(tmp_dir_name)
        return '/'.join(root_app_dir)

    def __split_document(self, tmp_dir_path) -> None:
        """
            Reads the document and save each page as a new doc.\n
            It changes working directory
        """
        os.chdir(tmp_dir_path)
        with open(self.original_pdf_filepath, 'rb') as pdf_descriptor:
            original_filename = self.__pdf_filename()
            pdf = PdfFileReader(pdf_descriptor)

            for page in range(pdf.getNumPages()):
                pdf_page_filename = f'{original_filename}_page_{page + 1}.pdf'
                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(pdf.getPage(page))

                with open(pdf_page_filename, 'wb') as outcoming_pdf:
                    pdf_writer.write(outcoming_pdf)

                print(f'-- Created: {pdf_page_filename}')
