import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from threading import Thread
from time import sleep
import automate_synchro_main as automate


class Call_dialog(QWidget):
    def __init__(self, establ_items, main_functions, value_fill, module="EMIF"):
        super().__init__()

        # To interact with local_xml fields
        self.value_fill = value_fill
        # To interact with main functions
        self.main_functions = main_functions
        self.module = module

        self.comboBox = QComboBox()
        self.comboBox.addItems(establ_items)
        self.number_of_notes = QSpinBox()
        self.button = QPushButton("OK")
        # 235x190
        self.label_establ = QLabel("Choose Establ:")
        self.label_no_notes = QLabel("Number of notes:")
        self.button.clicked.connect(self.automate_execute_n)
        layout = QVBoxLayout()
        layout.addWidget(self.label_establ)
        layout.addWidget(self.comboBox)
        layout.addWidget(self.label_no_notes)
        layout.addWidget(self.number_of_notes)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.setWindowTitle(f"Settings: {module}")
        self.setMinimumSize(265, 190)

    """ def call_fiscal_auto(self):
        while True:
            get_establ = self.comboBox.currentText()
            notes_no = self.number_of_notes.value()
            # global n_num
            # get_num = n_num.get()
            get_num_spin = int(self.number_of_notes.value())
            print("here's spin number", get_num_spin)
            try:
                automate.window_restore(w_spotted=get_establ, module_str=self.module)
                finished_status = automate.retrieve_dfe_keys(
                    w_get=get_establ, notes_ahead=get_num_spin, note_widget=notes_no
                )
                # notes_no.event_generate("<Decrement>")  # bad event type or keysym "Decrement"

                if finished_status == True:  # Maybe this status isn't budging
                    print(finished_status)
                    print("status?", finished_status)
                    self.custom_msg_box(save_ref=automate.retrieved_dfe_txt)

            except IndexError:
                QMessageBox.critical(
                    self,
                    "Corresponding Window not found!",
                    f"Unable to find corresponding window for: {get_establ}.\n\n Make Sure Synchro is launched at module: '{module}' \n 'Digitação/Manutenção de Documentos Fiscais' \n Estabelecimento: {get_establ}'.",
                )
            break """

    def call_emif_auto_n(self):
        while True:
            get_establ = self.comboBox.currentText()
            # global n_num
            # get_num = n_num.get()
            get_num_spin = int(self.number_of_notes.value())

            print("here's spin number", get_num_spin)
            try:
                for number in range(get_num_spin):
                    input_values = [
                        self.value_fill.pedido_combo.currentText(),
                        self.value_fill.nf_entry_combo.currentText(),
                        self.value_fill.ipi_edit.text(),
                        self.value_fill.qtd_edit.text(),
                        self.value_fill.total_edit.text(),
                        self.value_fill.val_unit_edit.text(),
                        self.value_fill.item_edit.text(),
                    ]
                    check = automate.copiar_nota()
                    if check == True:
                        sleep(0.2)
                        check = automate.edit_msg_single_shot(
                            values_in=input_values, establ_in=get_establ
                        )

                        if check == True:
                            # For some reason this gets ignored at times...
                            sleep(0.2)
                            if get_establ == "C&A0050FX":
                                check = automate.alterar_valores(
                                    input_values, is_rj_establ=True
                                )
                            else:
                                check = automate.alterar_valores(input_values)
                            if check == True:
                                sleep(0.5)
                                return_status = automate.totalizar_enviar()
                                if return_status == True:
                                    cur_val = self.number_of_notes.value()
                                    self.number_of_notes.setValue(cur_val - 1)
                                    self.main_functions.next_xml()  # is this enough?
                                    # this conflicts with thread and crashes
                                    # self.number_of_notes.stepDown()

                    if number == get_num_spin:
                        # this conflicts with thread and crashes
                        # self.number_of_notes.setValue(1)
                        break
            except Exception as e:
                QMessageBox.critical(self, "Error", "Unable to launch: " + str(e))
            if get_num_spin == 0 or IndexError:
                break

    def call_emif_auto(self):
        while True:
            get_establ = self.comboBox.currentText()
            # global n_num
            # get_num = n_num.get()
            get_num_spin = int(self.number_of_notes.value())

            print("here's spin number", get_num_spin)
            try:
                automate.window_restore(get_establ)
                for number in range(get_num_spin):
                    input_values = [
                        self.value_fill.pedido_combo.currentText(),
                        self.value_fill.nf_entry_combo.currentText(),
                        self.value_fill.ipi_edit.text(),
                        self.value_fill.qtd_edit.text(),
                        self.value_fill.total_edit.text(),
                        self.value_fill.val_unit_edit.text(),
                        self.value_fill.item_edit.text(),
                    ]
                    check = automate.copiar_nota()
                    if check == True:
                        sleep(0.2)
                        check = automate.edit_msg_single_shot(
                            values_in=input_values, establ_in=get_establ
                        )

                        if check == True:
                            # For some reason this gets ignored at times...
                            sleep(0.2)
                            if get_establ == "C&A0050FX":
                                check = automate.alterar_valores(
                                    input_values, is_rj_establ=True
                                )
                            else:
                                check = automate.alterar_valores(input_values)
                            if check == True:
                                sleep(0.5)
                                return_status = automate.totalizar_enviar()
                                if return_status == True:
                                    cur_val = self.number_of_notes.value()
                                    self.number_of_notes.setValue(cur_val - 1)
                                    self.main_functions.next_xml()  # is this enough?
                                    # this conflicts with thread and crashes
                                    # self.number_of_notes.stepDown()

                    if number == get_num_spin:
                        # this conflicts with thread and crashes
                        # self.number_of_notes.setValue(1)
                        break
            except IndexError:
                """error_title = "Corresponding Window not found!".encode()
                error_message = f"Unable to find corresponding window for: {get_establ}.\n\n Make Sure Synchro is launched at module: '{self.module}' \n 'Digitação/Manutenção de Documentos Fiscais' \n Estabelecimento: {get_establ}'.".encode()
                QMetaObject.invokeMethod(
                    self,
                    "show_error_message",
                    Qt.QueuedConnection,
                    error_title,
                    error_message,
                    Qt.AutoConnection,
                )"""
                QMessageBox.critical(
                    self,
                    "Janela Correspondente não encontrada!",
                    f"Não foi possível encontrar a janela referente á: {get_establ}.\n\n Certifique-se que o Synchro esteja aberto no modulo: '{self.module}' \n 'Digitação/Manutenção de Documentos Fiscais' \n Estabelecimento: {get_establ}'.",
                )
            if get_num_spin == 0 or IndexError:
                break

    def automate_execute_n(self):
        try:
            get_establ = self.comboBox.currentText()
            automate.window_restore(
                module_str=self.module, w_spotted=get_establ
            )  # wasn't module meant to be here?
            paralel_t = Thread(target=self.call_emif_auto_n, daemon=True)
            paralel_t.start()
        except IndexError:
            QMessageBox.critical(
                self,
                "Janela Correspondente não encontrada!",
                f"Não foi possível encontrar a janela referente á: {get_establ}.\n\n Certifique-se que o Synchro esteja aberto no modulo: '{self.module}' \n 'Digitação/Manutenção de Documentos Fiscais' \n Estabelecimento: {get_establ}'.",
            )

    def automate_execute(self):
        try:
            if self.module == "EMIF":
                paralel_t = Thread(target=self.call_emif_auto, daemon=True)
            # elif self.module == "FISCAL":
            # paralel_t = Thread(target=self.call_fiscal_auto, daemon=True)
            paralel_t.start()
        except Exception:
            QMessageBox.critical(self, "Error", message="Unable to launch")

        """ text = self.comboBox.currentText()
        self.mainWindow = MainWindow(text)
        self.mainWindow.show()
        self.close() """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Call_dialog()
    dialog.show()
    sys.exit(app.exec_())
