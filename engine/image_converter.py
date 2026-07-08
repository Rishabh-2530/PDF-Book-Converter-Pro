import fitz
import os


class ImageConverter:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)

    def export_page(
        self,
        page_number,
        output_path,
        zoom=4,
        image_format="png"
    ):

        page = self.doc.load_page(page_number)

        matrix = fitz.Matrix(zoom, zoom)

        pix = page.get_pixmap(matrix=matrix)

        if image_format.lower() == "jpg":
            pix.save(output_path, jpg_quality=100)
        else:
            pix.save(output_path)

    def export_all_pages(
        self,
        output_folder,
        zoom=4,
        image_format="png"
    ):

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        total_pages = len(self.doc)

        for page_number in range(total_pages):

            extension = image_format.lower()

            filename = f"page_{page_number + 1}.{extension}"

            output_path = os.path.join(
                output_folder,
                filename
            )

            self.export_page(
                page_number,
                output_path,
                zoom,
                image_format
            )

    def close(self):

        if self.doc:
            self.doc.close()