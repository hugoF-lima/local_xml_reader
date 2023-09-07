from collect_data_pane_qt import Ui_CollectDataPane
import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import qdarkstyle
from data_filter_openpyxl import collect_data, source_data
import automate_synchro_main
import automate_synchro_collect

from threading import Thread

# from subprocess import Popen
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import time

# Increase by 1 the loop total of collect data
# So unfortunately the filter is not without fail.
# Gonna have to make condition out of it also
# It apparently grabs wrong date from the field.
# (almost as if the variable data wasn't preserved?)


class Collect_data_main(QWidget):
    def __init__(self):
        super().__init__()
        cfop_list = ["5.949", "6.949"]
        establ_list = ["C&A0020FX", "C&A0093SC", "C&A0050FX"]

        self.ui = Ui_CollectDataPane()
        central_widget = QFrame(self)
        self.ui.setupUi(central_widget)
        self.setWindowTitle("Coletar dados do 'Fiscal' ")
        self.ui.collect_data_btn.setEnabled(False)
        self.ui.nat_op_button.setEnabled(False)
        self.ui.notes_no_spin.setEnabled(False)
        self.ui.notes_no_spin.setEnabled(True)

        self.ui.query_data_btn.clicked.connect(self.call_query_data)
        self.ui.collect_data_btn.clicked.connect(self.call_collect_thread)
        self.ui.cfop_combo.addItems(cfop_list)
        self.ui.establ_combo.addItems(establ_list)

    """ def eventFilter(self, obj, e):
        if obj.isWidgetType() and e.type() == e.WindowStateChange:
            if obj.windowState() & Qt.WindowMinimized:
                print("Minimized")
                # obj.showMaximized()

        return False """

    def qt_restore_win(self):
        self.showMinimized()
        self.setWindowState(
            self.windowState() and (not Qt.WindowMinimized or Qt.WindowActive)
        )

    def if_already_opened(self):
        if self.windowState() == Qt.WindowMinimized:
            # Window is minimised. Restore it.
            self.setWindowState(Qt.WindowNoState)
        else:
            self.call_main()

    def show_error_popup(self, value):
        mesg = QMessageBox()  # mesg.setStyleSheet("color: #888a85;")
        mesg.setWindowTitle("Janela Synchro não encontrada")
        mesg.setText(
            f"Não foi possível encontrar janela correspondente á {value} \n - Certifique-se que o Synchro esteja aberto no modulo 'Fiscal' para o establ. {value}"
        )
        mesg.setIcon(QMessageBox.Critical)
        mesg.raise_()
        x = mesg.exec_()

    # TODO: Make it mark an underline when highlighting informative_Text
    def show_info_popup(self):
        sheet = source_data.split(sep="\\")[-1]

        # if default_val == "information":

        # mesg.add
        # mesg.setInformativeText(f"<FONT COLOR='#07a8ff'><FONT SIZE='5'>{sheet}</FONT>")
        # mesg.setStyleSheet("QLabel::hover" "{" "background-color : lightgreen;" "}")

        """ for label in mesg.findChildren(QLabel):
            if label == "qt_msgbox_informativelabel":
                print(label)
        mesg.setStyleSheet(
            "QLabel::hover"
            "{"
            "font-weight: bold; color: green; text-decoration: underline"
            "}"
        ) """

        msgBox = QMessageBox()
        # msgBox.setText("Successfully saved to:")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setWindowTitle("Information")
        msgBox.setIcon(QMessageBox.Information)
        text_label = QLabel("Successfully saved to:")
        text_label.setAlignment(Qt.AlignCenter)

        # Custom widget
        class HoverLabel(QLabel):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setText(f"{sheet}")
                self.setFixedSize(170, 50)
                self.setCursor(Qt.PointingHandCursor)
                self.setAlignment(Qt.AlignCenter)
                self.setStyleSheet(
                    "QLabel {color: #07a8ff;} QLabel:hover {color: red;}"
                )

            def enterEvent(self, event):
                self.setStyleSheet("QLabel {color: red;}")

            def leaveEvent(self, event):
                self.setStyleSheet("QLabel {color: #07a8ff;}")

        label = HoverLabel()

        def on_label_clicked():
            print("Label clicked!")

        label.mousePressEvent = on_label_clicked

        # Add custom widget to the message box
        layout = QVBoxLayout()
        layout.addWidget(text_label)
        layout.addWidget(label)
        widget = QWidget()
        widget.setLayout(layout)
        msgBox.layout().addWidget(widget, 0, Qt.AlignCenter)
        msgBox.raise_()
        x = msgBox.exec_()

        # msgGeo = QRect(QPoint(0, 0), mesg.sizeHint())
        # x = mesg.exec_()

    def collect_data_start(self):
        # TODO: take out this redundancy

        list_val = [
            self.ui.notes_no_spin.value(),
            self.ui.establ_combo.currentText(),
            self.ui.nat_op_entr.text(),
            self.ui.fato_gerador_edit.text(),
            int(self.ui.cfop_combo.currentText().replace(".", "")),
        ]

        collect_data(
            cfop_val=list_val[4],
            data_emit=list_val[3],
            notes_ahead=list_val[0],
            w_get=list_val[1],
            widget_spin=self.ui.notes_no_spin,
        )

    def call_query_data(self):
        # When the notes take too long to appear,
        # It shows "not found"
        list_val = [
            self.ui.establ_combo.currentText(),
            self.ui.nat_op_entr.text(),
            self.ui.fato_gerador_edit.text(),
            self.ui.cfop_combo.currentText(),
        ]
        print(list_val)
        while True:
            try:
                automate_synchro_main.window_restore(
                    w_spotted=list_val[0], module_str="FISCAL"
                )

                result = automate_synchro_collect.query_notes(
                    cfop=list_val[3], nat_op=list_val[1], fato_gerador=list_val[2]
                )
                if result == True:
                    time.sleep(0.8)
                    self.qt_restore_win()
                    self.ui.collect_data_btn.setEnabled(True)
                    self.ui.notes_no_spin.setEnabled(True)
                else:
                    # self.setWindowState(Qt.WindowNoState)
                    # self.eventFilter()
                    # self.setWindowFlags(Qt.WindowStaysOnTopHint)
                    self.qt_restore_win()
                    self.show_error_popup(QMessageBox.Critical)
            except IndexError:
                self.show_error_popup(list_val[0])
            break

    def call_collect_thread(self):
        try:
            paralel_t = Thread(target=self.collect_data_start, daemon=True)
            paralel_t.start()
        except Exception:
            pass
        # self.show_error_popup(QMessageBox.Information)

    """ def call_main(self):
        self.show() """

    def call_main(self):
        if self.windowState() == Qt.WindowMinimized:
            # Window is minimised. Restore it.
            self.setWindowState(Qt.WindowNoState)
        else:
            self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    demo = Collect_data_main()
    demo.call_main()
    sys.exit(app.exec_())
