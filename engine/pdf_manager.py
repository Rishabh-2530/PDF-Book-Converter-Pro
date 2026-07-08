import fitz
from PySide6.QtGui import QPixmap, QImage


class PDFManager:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)

    def page_count(self):
        return len(self.doc)

    def page_size(self, page_number):
        page = self.doc.load_page(page_number)
        rect = page.rect
        return int(rect.width), int(rect.height)

    def render_page(self, page_number, zoom=2):

        page = self.doc.load_page(page_number)

        matrix = fitz.Matrix(zoom, zoom)

        pix = page.get_pixmap(matrix=matrix)

        if pix.alpha:
            fmt = QImage.Format_RGBA8888
        else:
            fmt = QImage.Format_RGB888

        image = QImage(
            pix.samples,
            pix.width,
            pix.height,
            pix.stride,
            fmt
        ).copy()

        return QPixmap.fromImage(image)

    def save_page_as_png(
        self,
        page_number,
        output_path,
        zoom=4
    ):

        page = self.doc.load_page(page_number)

        matrix = fitz.Matrix(zoom, zoom)

        pix = page.get_pixmap(matrix=matrix)

        pix.save(output_path)

    def export_all_pages(
        self,
        output_folder,
        zoom=4
    ):

        total = len(self.doc)

        for i in range(total):

            page = self.doc.load_page(i)

            matrix = fitz.Matrix(zoom, zoom)

            pix = page.get_pixmap(matrix=matrix)

            output_file = (
                f"{output_folder}/page_{i+1}.png"
            )

            pix.save(output_file)

    def export_page_range(
        self,
        start_page,
        end_page,
        output_folder,
        zoom=4
    ):
            if start_page < 1:
            start_page = 1

        if end_page > len(self.doc):
            end_page = len(self.doc)

        for i in range(start_page - 1, end_page):

            page = self.doc.load_page(i)

            matrix = fitz.Matrix(zoom, zoom)

            pix = page.get_pixmap(matrix=matrix)

            output_file = (
                f"{output_folder}/page_{i+1}.png"
            )

            pix.save(output_file)

    def get_document(self):
        return self.doc

    def get_page(self, page_number):
        return self.doc.load_page(page_number)

    def close(self):

        if self.doc:
            self.doc.close()