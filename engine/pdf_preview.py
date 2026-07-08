import fitz  # PyMuPDF

from PySide6.QtGui import QPixmap, QImage


class PDFPreview:

    @staticmethod
    def load_pdf(pdf_path):

        doc = fitz.open(pdf_path)

        total_pages = len(doc)

        page = doc.load_page(0)

        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        image = QImage(
            pix.samples,
            pix.width,
            pix.height,
            pix.stride,
            QImage.Format_RGB888,
        )

        preview = QPixmap.fromImage(image)

        return preview, total_pages