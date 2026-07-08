import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
)

from engine.pdf_preview import PDFPreview


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.current_page = 1
        self.total_pages = 0
        self.current_pdf = ""
        self.zoom = 1.0

        self.setWindowTitle("PDF Book Converter Pro")
        self.resize(1100, 750)

        # ===========================
        # Central Widget
        # ===========================

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        # ===========================
        # Toolbar
        # ===========================

        toolbar = QHBoxLayout()

        self.select_btn = QPushButton("📂 Select PDF")
        self.select_btn.setFixedHeight(40)
        self.select_btn.clicked.connect(self.select_pdf)

        self.prev_btn = QPushButton("⬅ Previous")
        self.prev_btn.setEnabled(False)

        self.page_info = QLabel("Page : 0 / 0")
        self.page_info.setAlignment(Qt.AlignCenter)

        self.next_btn = QPushButton("Next ➡")
        self.next_btn.setEnabled(False)

        self.zoom_out_btn = QPushButton("➖")

        self.zoom_label = QLabel("100%")

        self.zoom_in_btn = QPushButton("➕")

        toolbar.addWidget(self.select_btn)
        toolbar.addSpacing(20)
        toolbar.addWidget(self.prev_btn)
        toolbar.addWidget(self.page_info)
        toolbar.addWidget(self.next_btn)
        toolbar.addStretch()
        toolbar.addWidget(self.zoom_out_btn)
        toolbar.addWidget(self.zoom_label)
        toolbar.addWidget(self.zoom_in_btn)

        self.layout.addLayout(toolbar)

        # ===========================
        # File Name
        # ===========================

        self.file_label = QLabel("📄 File Name : No PDF Selected")
        self.file_label.setStyleSheet("font-size:16px;")
        self.layout.addWidget(self.file_label)

        # ===========================
        # Total Pages
        # ===========================

        self.page_label = QLabel("📑 Total Pages : 0")
        self.page_label.setStyleSheet("font-size:16px;")
        self.layout.addWidget(self.page_label)

        title = QLabel("🖼 First Page Preview")
        title.setStyleSheet("font-size:18px;font-weight:bold;")
        self.layout.addWidget(title)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(500)
        self.preview_label.setStyleSheet("""
            border:2px solid gray;
            background:white;
        """)
        self.preview_label.setText("Preview will appear here")
        self.layout.addWidget(self.preview_label)

        self.status_label = QLabel("🟢 Status : Waiting for PDF...")
        self.status_label.setStyleSheet("color:green;font-size:15px;")
        self.layout.addWidget(self.status_label)
            # =================================================
    # Select PDF
    # =================================================

    def select_pdf(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        self.current_pdf = file_path

        try:

            preview, total_pages = PDFPreview.load_pdf(file_path)

            self.total_pages = total_pages
            self.current_page = 1

            self.file_label.setText(
                f"📄 File Name : {os.path.basename(file_path)}"
            )

            self.page_label.setText(
                f"📑 Total Pages : {self.total_pages}"
            )

            self.page_info.setText(
                f"Page : {self.current_page} / {self.total_pages}"
            )

            self.preview_label.setPixmap(
                preview.scaled(
                    700,
                    500,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

            self.status_label.setText(
                "✅ PDF Loaded Successfully"
            )

            self.prev_btn.setEnabled(False)

            if self.total_pages > 1:
                self.next_btn.setEnabled(True)
            else:
                self.next_btn.setEnabled(False)

        except Exception as e:

            self.status_label.setStyleSheet(
                "color:red;font-size:15px;"
            )

            self.status_label.setText(
                "❌ Error Opening PDF"
            )

            print(e)

    # =================================================
    # Previous Page
    # =================================================

    def previous_page(self):

        if self.current_page <= 1:
            return

        self.current_page -= 1

        self.page_info.setText(
            f"Page : {self.current_page} / {self.total_pages}"
        )

    # =================================================
    # Next Page
    # =================================================

    def next_page(self):

        if self.current_page >= self.total_pages:
            return

        self.current_page += 1

        self.page_info.setText(
            f"Page : {self.current_page} / {self.total_pages}"
        )