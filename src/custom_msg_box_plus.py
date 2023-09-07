from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
import base64
from subprocess import Popen
from outline_label import *
import qdarkstyle
import os

info_icon = b"iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA7NpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wUmlnaHRzPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvcmlnaHRzLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcFJpZ2h0czpNYXJrZWQ9IkZhbHNlIiB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6QUVDMDI4MTkwRTY3REYxMThENDY4Njc1NDgyMTlCRTAiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6NkM1M0ZDMDNEQUQ0MTFERjg4NEZENTZCRURFQUVGQUQiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6NkM1M0ZDMDJEQUQ0MTFERjg4NEZENTZCRURFQUVGQUQiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6OEYwRUMwNDNDRURBREYxMTg0RUJCOTg3RjExQTQxOUUi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"


# This code uses the outline_label special class
# Hence a bit different from standard examples
class CustomDialog(QDialog):
    def __init__(self, rfid_path):
        super().__init__()

        self.rfid_path = rfid_path
        self.setWindowTitle("Sucess!")
        # self.setGeometry(100, 100, 460, 107)

        # Decode base64 to QImage object
        image_data = base64.b64decode(info_icon)
        image = QImage.fromData(image_data)
        # Create a QPixmap object from the QImage object
        pixmap = QPixmap.fromImage(image)

        self.message_user = QLabel("Salvo em:")

        self.info_icon = QLabel()
        self.info_icon.setMinimumSize(60, 50)  # visible area
        self.icon = QIcon(pixmap)  # Use built-in icon name, such as "help-about"
        self.info_icon.setPixmap(self.icon.pixmap(50, 50))  # Sixe of pixmap
        self.info_icon.setScaledContents(False)

        # rfid_name = self.display_base_name(rfid_path)
        self.info_path = OutlinedLabel(self.display_base_name(rfid_path))
        self.info_path.setPen(Qt.blue)
        self.info_path.setBrush(Qt.gray)

        # Set label boundaries
        # self.info_path.setMinimumSize(20, 20)  # Set minimum size to 200x50 pixels
        # self.info_path.setMaximumSize(60, 20)  # Set maximum size to 400x100 pixels
        # self.info_path.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        # self.info_path.setAlignment(Qt.AlignLeft)
        self.info_path.setMaximumWidth(10)

        layout_sub = QHBoxLayout(self)
        layout_sub.addWidget(self.info_icon)
        layout_sub.addWidget(self.message_user)
        layout_sub.addWidget(self.info_path)
        layout_sub.setStretch(0, 0)  # set stretch factor for icon label to 0
        layout_sub.setStretch(1, 0)  # set stretch factor for message label to 0
        layout_sub.setStretch(2, 1)  # set stretch factor for path label to 1

        """ layout_sub = QHBoxLayout(self)
        layout_sub.setStretchFactor(self.info_path, 10)
        layout_sub.addWidget(self.info_icon)
        layout_sub.addWidget(self.message_user)
        layout_sub.addWidget(self.info_path) """

        # layout_sub.setContentsMargins(0, 0, 0, 0)

        """ layout = QVBoxLayout(self)
        layout.addLayout(layout_sub) """
        # print(QIcon.hasThemeIcon("help-about"))

        # Allow the label to expand to fill available space

        # Set initial color to black
        self.message_user.setStyleSheet("font: 12pt 'MS Shell Dlg 2;'")
        self.info_path.setStyleSheet("font: 12pt 'MS Shell Dlg 2'")

        # Connect signals
        # self.label.mousePressEvent = self.label_pressed
        self.info_path.mousePressEvent = self.label_pressed
        self.info_path.mouseReleaseEvent = self.label_released
        self.info_path.enterEvent = self.label_hovered
        self.info_path.leaveEvent = self.label_unhovered

    def display_base_name(self, file_path):
        file_name = os.path.basename(file_path)
        file_name_without_ext = os.path.splitext(file_name)[0]
        return file_name_without_ext

    def label_hovered(self, event):
        self.info_path.setStyleSheet(
            "font: 12pt 'MS Shell Dlg 2'; border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px;"
        )
        self.info_path.setPen(Qt.darkCyan)
        self.info_path.setBrush(Qt.gray)

    def label_unhovered(self, event):
        self.info_path.setStyleSheet("font: 12pt 'MS Shell Dlg 2';")
        self.info_path.setPen(Qt.blue)
        self.info_path.setBrush(Qt.gray)

    def label_pressed(self, event):
        self.info_path.setStyleSheet("font: 12pt 'MS Shell Dlg 2';")
        self.info_path.setPen(Qt.red)
        self.info_path.setBrush(Qt.gray)
        e = Popen(rf'explorer /select,"{self.rfid_path}"')

    def label_released(self, event):
        self.info_path.setStyleSheet(
            "font: 12pt 'MS Shell Dlg 2'; color: blue; border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px;"
        )
        self.info_path.setPen(Qt.darkCyan)
        self.info_path.setBrush(Qt.gray)
        self.close()

    def resizeEvent(self, event):
        self.info_path.setFixedSize(self.info_path.sizeHint())
        self.message_user.setFixedSize(self.info_path.sizeHint())
        # self.info_icon.setFixedSize(self.info_path.sizeHint())


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    rfid_path = r"src\02-Feb_2023\synchro_automation_rev_2\local_rfid.xlsx"  # 2 pixels to correct visual glitch
    dialog = CustomDialog(rfid_path)
    dialog.show()
    app.exec_()
