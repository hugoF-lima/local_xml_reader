import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import qdarkstyle
from local_xml_reader import Ui_local_xml_reader
from call_automate import Call_dialog
from data_collect_main import *
from pandas import DataFrame
from custom_msg_box_plus import CustomDialog
from read_xml_data import (
    populate_fields,
    read_in_xml_data,
    save_xml_to_excel,
    unzip_contents,
    rfid_sheet,
)
from subprocess import Popen
from os import remove


class Local_xml_call(QWidget):
    def __init__(self):
        super().__init__()
        # TODO: I believe this call other windows at once.
        # Slowing down the application perharps.
        """ self.ui = Ui_local_xml_reader()
        central_widget = QFrame(self)
        central_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )  # set size policy
        self.ui.setupUi(central_widget)
        self.setWindowTitle("Ferramental RFID") """
        self.setWindowTitle("Ferramental RFID")

        # Create a new QWidget instance and set the Ui_local_xml_reader widget as its child
        self.widget = QWidget(self)
        self.ui = Ui_local_xml_reader()
        self.ui.setupUi(self.widget)
        # Set the size policy of the widget to expanding
        self.widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Create a QVBoxLayout instance and add the widget to it
        layout = QVBoxLayout(self)
        layout.addWidget(self.widget)
        # Set the layout of the main window
        self.setLayout(layout)

        self.incr_decr = int(0)  # One of the data attrib's
        self.nnf_total = int(0)
        self.nnf_pandas = ""
        self.nnf_pandas += f"{self.incr_decr} of {self.nnf_total}"
        self.set_string(widget_in=self.ui.lbl_counter, value=self.nnf_pandas)

        self.default_establs = ["C&A0020FX", "C&A0093SC", "C&A0050FX"]

        self.ini_file = r"defaults.ini"

        self.cols_use = [
            "Nota Entrada",
            "Item",
            "Quantidade",
            "Val_Unitario",
            "Total Nota",
            "Fornecedor",  # this is important
            "IPI",
            "Pedido",
            "Data Emissão",  # Unused on display
            "Emissor",  # Unused on display
            "CNPJ",  # 10 (?)
        ]

        self.ui.enable_automate_btn.setEnabled(True)

        self.data_grid = DataFrame()  # Lacking?
        self.pick_folder = ""

        self.ui.load_xml_btn.clicked.connect(self.read_and_populate)
        self.ui.save_excel_btn.clicked.connect(self.save_it_to_excel)

        self.ui.next_xml_btn.clicked.connect(self.next_xml)
        self.ui.prev_xml_btn.clicked.connect(self.prev_xml)
        self.ui.jump_first_btn.clicked.connect(self.jump_first_xml)
        self.ui.jump_last_btn.clicked.connect(self.jump_last_xml)

        self.ui.nf_entry_combo.currentIndexChanged.connect(self.filter_combo)
        self.ui.pedido_combo.currentIndexChanged.connect(self.filter_combo)
        self.ui.fornecedor_combo.currentIndexChanged.connect(self.filter_combo)

        self.ui.enable_automate_btn.clicked.connect(self.call_automate_pane)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_menu)

    def right_menu(self, pos):
        menu = QMenu()

        # Add menu options
        extract_df_option = menu.addAction("Extrair chaves Dfe...")
        copy_link_option = menu.addAction("Copiar Link do Web Synchro")

        open_rfid_sheet = menu.addAction("Abrir planilha RFID")
        extract_data = menu.addAction("Extrair Dados do 'Fiscal'")
        # exit_option = menu.addAction("Exit")

        # Menu option events
        extract_df_option.triggered.connect(lambda: self.run_df_key_extract())
        copy_link_option.triggered.connect(lambda: print("Goodbye"))
        extract_data.triggered.connect(lambda: self.run_qt_collect())
        open_rfid_sheet.triggered.connect(
            lambda: Popen(rf'explorer /select,"{rfid_sheet}"')
        )
        # exit_option.triggered.connect(lambda: exit())

        # Position
        menu.exec_(self.mapToGlobal(pos))

    def run_df_key_extract():
        pass

        # TODO: Restore window if visible

    def run_qt_collect(self):
        self.ui_2 = Collect_data_main()
        self.ui_2.if_already_opened()

        # x = app.exec_()

    def call_dialog_thread(self):
        self.ui_3 = Call_dialog(
            establ_items=self.default_establs, main_functions=self, value_fill=self.ui
        )
        self.ui_3.show()

    def alternate_thread_start(self):
        try:
            paralel_t = Thread(target=self.call_dialog_thread, daemon=True)
            # elif self.module == "FISCAL":
            # paralel_t = Thread(target=self.call_fiscal_auto, daemon=True)
            paralel_t.start()
        except Exception as e:
            QMessageBox.critical(self, "Error", "Unable to launch: " + str(e))

    def call_automate_pane(self):
        # grab relevant parameters through here
        # Relevant getters and setters to the rescue
        # In older times, encapsulating through getters and setters was a thing.
        # Perhaprs this could solve the threading issue of pyqt
        self.ui_3 = Call_dialog(
            establ_items=self.default_establs, main_functions=self, value_fill=self.ui
        )
        self.ui_3.show()

    def set_string(self, widget_in, value):
        widget_in.setText(value)

    def combo_index_state(self):
        # the issue here is that, the button triggers
        # operation in all comboboxes at once.

        # the issue might be the change event itself.
        # change event might need to issue
        # another behavior to the widgets instead...

        # current behavior is always updating directly from xml.

        sender = self.sender()
        if sender == self.ui.pedido_combo:
            self.incr_decr = int(self.ui.pedido_combo.currentIndex())
            print("Does this fire?", self.incr_decr)
        elif sender == self.ui.nf_entry_combo:
            self.incr_decr = int(self.ui.nf_entry_combo.currentIndex())
            print("Does this fire?", self.incr_decr)
        else:
            self.incr_decr = int(self.ui.fornecedor_combo.currentIndex())
            print("Does this fire?", self.incr_decr)

        return self.incr_decr

    def filter_combo(self):
        def filter_event(val_in):
            self.change_event(val_in)

        sender = self.sender()  # qtcore bind
        if sender == self.ui.fornecedor_combo:
            val_in = self.ui.fornecedor_combo.currentIndex()
            self.incr_decr = val_in
            filter_event(val_in)
        elif sender == self.ui.nf_entry_combo:
            val_in = self.ui.nf_entry_combo.currentIndex()
            self.incr_decr = val_in
            filter_event(val_in)
        elif sender == self.ui.pedido_combo:
            val_in = self.ui.pedido_combo.currentIndex()
            self.incr_decr = val_in
            filter_event(val_in)

    def jump_last_xml(self):
        self.incr_decr = self.nnf_total
        combo_box_adjuster = self.nnf_total
        self.change_event(combo_box_adjuster)

    def next_xml(self):
        self.incr_decr += 1
        self.change_event(self.incr_decr)

    def jump_first_xml(self):
        self.incr_decr = 1
        combo_box_adjuster = self.incr_decr
        self.change_event(combo_box_adjuster)

    def prev_xml(self):
        self.incr_decr -= 1
        print("value_in", self.incr_decr)
        self.change_event(self.incr_decr)

    def return_path(self):  # I'll experiment on this in a sec
        store_path = ""
        if self.pick_folder == "":
            self.pick_folder = self.first_access()
        if self.pick_folder != None:
            store_path += self.pick_folder
            return store_path

    def save_it_to_excel(self):
        # TODO: Make some path handler for File not Found
        #'Associate New File' button
        pick_folder = self.return_path()
        # The above is finally working huh
        appended_data = read_in_xml_data(pick_folder)
        print(appended_data)
        try:
            save_xml_to_excel(appended_data)  # Since this only grabs each row
            # TODO: Set link to path as the older software did
            self.ui_4 = CustomDialog(rfid_sheet)
            self.ui_4.show()
            # QMessageBox.information(self, "Success", f"Successfully saved {rfid_sheet}"

        except FileNotFoundError as notfound:
            QMessageBox.critical(
                self,
                "Error",
                "Arquivo Não Encontrado! \n Cheque o Caminho! \n Detalhe tecnico: {}".format(
                    notfound
                ),
            )
        except PermissionError as noperm:
            QMessageBox.critical(
                self,
                "Não foi possível gravar na planilha",
                "Não foi possível gravar, Certifique-se que ela esteja fechada!\n Detalhe tecnico: {}".format(
                    noperm
                ),
            )
        except Exception as unkwnown:
            print(unkwnown)
            """ QMessageBox.critical(
                self,
                "Unknown Error",
                "Unexpected Error occured\n Error Details: {}".format(
                    unkwnown.with_traceback
                ),
            ) """
        # messagebox.showinfo(title="Salvo!", message=f"salvo em: {rfid_sheet}")

    def start_py_auto(self):
        pass

    def read_and_populate(self):  # gonna have to chain here
        stored_path = self.pick_folder
        self.pick_folder = self.first_access()
        if self.pick_folder != None:
            self.zero_labels()  # Because labels need their own tree for erasing
            # call the main populate
            self.incr_decr += 1
            self.nnf_total = self.change_event(value_change=self.incr_decr)
            self.ui.nf_entry_combo.setCurrentIndex(1)
            self.ui.pedido_combo.setCurrentIndex(1)
            self.ui.fornecedor_combo.setCurrentIndex(1)
            self.nnf_pandas = ""
            self.nnf_pandas = f"{self.incr_decr} of {self.nnf_total}"
            self.set_string(widget_in=self.ui.lbl_counter, value=self.nnf_pandas)
            # I wonder if moving it here would do
        elif self.pick_folder == None:
            self.pick_folder = stored_path

    def first_access(self):
        # Somehow this is not saving previous path assign.
        print("current folder", self.pick_folder)
        pick_it = QFileDialog.getExistingDirectory(self, "Selecione a pasta do XML")
        # specify initial dir?
        print(pick_it)
        if pick_it != "":
            zip_obj = unzip_contents(pick_it)
            if zip_obj:  # because sometimes you might open an empty folder
                if str(zip_obj[-1]).endswith(".zip"):
                    # given remove is blind to file_type
                    remove(zip_obj[-1])
            # Because returns wrap on lists
            # And the structure always leave the zip path at the last...
            return pick_it

    def zero_labels(self):
        self.incr_decr = 0
        self.nnf_total = 0
        self.nnf_pandas = ""
        self.nnf_pandas += f"{self.incr_decr} of {self.nnf_total}"
        self.set_string(widget_in=self.ui.lbl_counter, value=self.nnf_pandas)

    def prev_btn_state(self, *widget):
        for w in widget:
            if self.incr_decr == 1:
                w.setEnabled(False)
            else:  # too primitive
                w.setEnabled(True)

    def next_btn_state(self, *widget):
        for w in widget:
            if self.incr_decr == self.nnf_total:
                w.setEnabled(False)
            else:  # too primitive
                w.setEnabled(True)

    def change_event(self, value_change):
        # qwidget_list = self.findChildren(QLineEdit) + self.findChildren(QComboBox)
        # Cleaning and loading xml data
        # So, the combobox object cannot be cleaned...
        # it loops until maximum recursion because of setIndexChanged...
        for widget in self.findChildren(QLineEdit):
            # print(num, widget)
            widget.clear()

        appended_data = read_in_xml_data(self.pick_folder)
        self.data_grid = DataFrame(data=appended_data, columns=self.cols_use)
        self.data_grid = self.data_grid.sort_values(
            by=["Fornecedor"],
            ascending=True,
            inplace=False,
            ignore_index=True,
        )

        # TODO: Autocomplete for QComboBox
        # self.ui.nf_entry_combo.setCurrentIndex(self.incr_decr)
        # self.ui.nf_entry_combo.currentIndex(self.incr_decr)
        # self.entry_nota.current(self.incr_decr)

        populate_fields(
            self.data_grid,
            self.ui.nf_entry_combo,
            self.ui.item_edit,
            self.ui.qtd_edit,
            self.ui.val_unit_edit,
            self.ui.cnpj_edit,
            self.ui.total_edit,
            self.ui.fornecedor_combo,
            self.ui.ipi_edit,
            self.ui.pedido_combo,  # search filters
            value_change,  # search filters
        )
        # Storing the first one
        # By logic, this should've been here...
        # self.nnf_total_s.set(f"{self.nnf_total}")  # I smell redundancy here
        self.nnf_pandas = ""
        self.nnf_pandas += f"{self.incr_decr} of {self.nnf_total}"
        self.set_string(widget_in=self.ui.lbl_counter, value=self.nnf_pandas)

        self.next_btn_state(self.ui.next_xml_btn, self.ui.jump_last_btn)
        self.prev_btn_state(self.ui.prev_xml_btn, self.ui.jump_first_btn)

        self.ui.save_excel_btn.setEnabled(True)
        # Monkey insertion? #A function to update would be neater
        self.ui.save_excel_btn.setEnabled(True)

        return self.data_grid.shape[0]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    instance = Local_xml_call()
    instance.show()
    sys.exit(app.exec_())
