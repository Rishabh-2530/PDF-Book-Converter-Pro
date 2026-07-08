import sys
from PySide6.QtWidgets import QApplication, QLabel, QPushButton
app = QApplication(sys.argv)

button = QPushButton("Select PDF")
button.setText("Select PDF")
button.resize(200, 60)
button.show()

app.exec()