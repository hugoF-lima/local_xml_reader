# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'local_xml_reader_attmpt_2.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_local_xml_reader(object):
    def setupUi(self, local_xml_reader):
        if not local_xml_reader.objectName():
            local_xml_reader.setObjectName(u"local_xml_reader")
        local_xml_reader.resize(498, 325)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(local_xml_reader.sizePolicy().hasHeightForWidth())
        local_xml_reader.setSizePolicy(sizePolicy)
        local_xml_reader.setWindowTitle(u"")
        self.gridLayout = QGridLayout(local_xml_reader)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(8, 0, 1, 7)
        self.item_edit = QLineEdit(local_xml_reader)
        self.item_edit.setObjectName(u"item_edit")

        self.gridLayout.addWidget(self.item_edit, 1, 0, 1, 5)

        self.qtd_edit = QLineEdit(local_xml_reader)
        self.qtd_edit.setObjectName(u"qtd_edit")

        self.gridLayout.addWidget(self.qtd_edit, 3, 0, 1, 5)

        self.lbl_counter = QLabel(local_xml_reader)
        self.lbl_counter.setObjectName(u"lbl_counter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lbl_counter.sizePolicy().hasHeightForWidth())
        self.lbl_counter.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(12)
        self.lbl_counter.setFont(font)
        self.lbl_counter.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lbl_counter, 12, 3, 1, 3)

        self.next_xml_btn = QPushButton(local_xml_reader)
        self.next_xml_btn.setObjectName(u"next_xml_btn")
        self.next_xml_btn.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.next_xml_btn.sizePolicy().hasHeightForWidth())
        self.next_xml_btn.setSizePolicy(sizePolicy2)
        self.next_xml_btn.setMinimumSize(QSize(50, 20))
        font1 = QFont()
        font1.setPointSize(10)
        self.next_xml_btn.setFont(font1)

        self.gridLayout.addWidget(self.next_xml_btn, 11, 5, 1, 1)

        self.ipi_edit = QLineEdit(local_xml_reader)
        self.ipi_edit.setObjectName(u"ipi_edit")

        self.gridLayout.addWidget(self.ipi_edit, 8, 0, 1, 5)

        self.save_excel_btn = QPushButton(local_xml_reader)
        self.save_excel_btn.setObjectName(u"save_excel_btn")
        self.save_excel_btn.setEnabled(False)
        self.save_excel_btn.setFont(font1)

        self.gridLayout.addWidget(self.save_excel_btn, 12, 1, 1, 1)

        self.lbl_nf_entry = QLabel(local_xml_reader)
        self.lbl_nf_entry.setObjectName(u"lbl_nf_entry")

        self.gridLayout.addWidget(self.lbl_nf_entry, 0, 5, 1, 1)

        self.lbl_val_unit = QLabel(local_xml_reader)
        self.lbl_val_unit.setObjectName(u"lbl_val_unit")

        self.gridLayout.addWidget(self.lbl_val_unit, 4, 5, 1, 1)

        self.fornecedor_combo = QComboBox(local_xml_reader)
        self.fornecedor_combo.setObjectName(u"fornecedor_combo")

        self.gridLayout.addWidget(self.fornecedor_combo, 7, 0, 1, 5)

        self.total_edit = QLineEdit(local_xml_reader)
        self.total_edit.setObjectName(u"total_edit")

        self.gridLayout.addWidget(self.total_edit, 6, 0, 1, 5)

        self.prev_xml_btn = QPushButton(local_xml_reader)
        self.prev_xml_btn.setObjectName(u"prev_xml_btn")
        self.prev_xml_btn.setEnabled(False)
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(70)
        sizePolicy3.setVerticalStretch(20)
        sizePolicy3.setHeightForWidth(self.prev_xml_btn.sizePolicy().hasHeightForWidth())
        self.prev_xml_btn.setSizePolicy(sizePolicy3)
        self.prev_xml_btn.setMinimumSize(QSize(50, 20))
        self.prev_xml_btn.setFont(font1)

        self.gridLayout.addWidget(self.prev_xml_btn, 11, 3, 1, 2)

        self.cnpj_edit = QLineEdit(local_xml_reader)
        self.cnpj_edit.setObjectName(u"cnpj_edit")

        self.gridLayout.addWidget(self.cnpj_edit, 5, 0, 1, 5)

        self.lbl_ipi = QLabel(local_xml_reader)
        self.lbl_ipi.setObjectName(u"lbl_ipi")

        self.gridLayout.addWidget(self.lbl_ipi, 8, 5, 1, 1)

        self.load_xml_btn = QPushButton(local_xml_reader)
        self.load_xml_btn.setObjectName(u"load_xml_btn")
        self.load_xml_btn.setFont(font1)

        self.gridLayout.addWidget(self.load_xml_btn, 11, 1, 1, 1)

        self.enable_automate_btn = QPushButton(local_xml_reader)
        self.enable_automate_btn.setObjectName(u"enable_automate_btn")
        self.enable_automate_btn.setEnabled(False)
        self.enable_automate_btn.setFont(font1)

        self.gridLayout.addWidget(self.enable_automate_btn, 11, 0, 1, 1)

        self.nf_entry_combo = QComboBox(local_xml_reader)
        self.nf_entry_combo.setObjectName(u"nf_entry_combo")

        self.gridLayout.addWidget(self.nf_entry_combo, 0, 0, 1, 5)

        self.lbl_qtd = QLabel(local_xml_reader)
        self.lbl_qtd.setObjectName(u"lbl_qtd")

        self.gridLayout.addWidget(self.lbl_qtd, 3, 5, 1, 1)

        self.pedido_combo = QComboBox(local_xml_reader)
        self.pedido_combo.setObjectName(u"pedido_combo")

        self.gridLayout.addWidget(self.pedido_combo, 9, 0, 1, 5)

        self.lbl_item = QLabel(local_xml_reader)
        self.lbl_item.setObjectName(u"lbl_item")

        self.gridLayout.addWidget(self.lbl_item, 1, 5, 1, 1)

        self.lbl_total = QLabel(local_xml_reader)
        self.lbl_total.setObjectName(u"lbl_total")

        self.gridLayout.addWidget(self.lbl_total, 6, 5, 1, 1)

        self.lbl_pedido = QLabel(local_xml_reader)
        self.lbl_pedido.setObjectName(u"lbl_pedido")

        self.gridLayout.addWidget(self.lbl_pedido, 9, 5, 1, 1)

        self.jump_last_btn = QPushButton(local_xml_reader)
        self.jump_last_btn.setObjectName(u"jump_last_btn")
        self.jump_last_btn.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.jump_last_btn.sizePolicy().hasHeightForWidth())
        self.jump_last_btn.setSizePolicy(sizePolicy3)
        self.jump_last_btn.setMinimumSize(QSize(50, 20))
        self.jump_last_btn.setFont(font1)
        self.jump_last_btn.setIconSize(QSize(16, 16))

        self.gridLayout.addWidget(self.jump_last_btn, 11, 6, 1, 1)

        self.jump_first_btn = QPushButton(local_xml_reader)
        self.jump_first_btn.setObjectName(u"jump_first_btn")
        self.jump_first_btn.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.jump_first_btn.sizePolicy().hasHeightForWidth())
        self.jump_first_btn.setSizePolicy(sizePolicy3)
        self.jump_first_btn.setMinimumSize(QSize(50, 20))
        self.jump_first_btn.setFont(font1)

        self.gridLayout.addWidget(self.jump_first_btn, 11, 2, 1, 1)

        self.load_xml_btn_3 = QPushButton(local_xml_reader)
        self.load_xml_btn_3.setObjectName(u"load_xml_btn_3")
        self.load_xml_btn_3.setEnabled(False)
        self.load_xml_btn_3.setFont(font1)

        self.gridLayout.addWidget(self.load_xml_btn_3, 12, 0, 1, 1)

        self.lbl_forn = QLabel(local_xml_reader)
        self.lbl_forn.setObjectName(u"lbl_forn")

        self.gridLayout.addWidget(self.lbl_forn, 7, 5, 1, 1)

        self.val_unit_edit = QLineEdit(local_xml_reader)
        self.val_unit_edit.setObjectName(u"val_unit_edit")

        self.gridLayout.addWidget(self.val_unit_edit, 4, 0, 1, 5)

        self.lbl_cnpj = QLabel(local_xml_reader)
        self.lbl_cnpj.setObjectName(u"lbl_cnpj")

        self.gridLayout.addWidget(self.lbl_cnpj, 5, 5, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 10, 0, 1, 1)


        self.retranslateUi(local_xml_reader)

        QMetaObject.connectSlotsByName(local_xml_reader)
    # setupUi

    def retranslateUi(self, local_xml_reader):
        self.lbl_counter.setText(QCoreApplication.translate("local_xml_reader", u"0 of 0", None))
        self.next_xml_btn.setText(QCoreApplication.translate("local_xml_reader", u">", None))
        self.save_excel_btn.setText(QCoreApplication.translate("local_xml_reader", u"Salvar na Planilha", None))
        self.lbl_nf_entry.setText(QCoreApplication.translate("local_xml_reader", u": Nf Entrada", None))
        self.lbl_val_unit.setText(QCoreApplication.translate("local_xml_reader", u": Val Unit (Qtd)", None))
        self.prev_xml_btn.setText(QCoreApplication.translate("local_xml_reader", u"<", None))
        self.lbl_ipi.setText(QCoreApplication.translate("local_xml_reader", u": IPI (ODA)", None))
        self.load_xml_btn.setText(QCoreApplication.translate("local_xml_reader", u"Carregar Pasta", None))
        self.enable_automate_btn.setText(QCoreApplication.translate("local_xml_reader", u"Habilitar Emiss\u00e3o", None))
        self.lbl_qtd.setText(QCoreApplication.translate("local_xml_reader", u": Qtd", None))
        self.lbl_item.setText(QCoreApplication.translate("local_xml_reader", u": Item", None))
        self.lbl_total.setText(QCoreApplication.translate("local_xml_reader", u": Total (R$)", None))
        self.lbl_pedido.setText(QCoreApplication.translate("local_xml_reader", u": Pedido", None))
        self.jump_last_btn.setText(QCoreApplication.translate("local_xml_reader", u">|", None))
        self.jump_first_btn.setText(QCoreApplication.translate("local_xml_reader", u"|<", None))
        self.load_xml_btn_3.setText(QCoreApplication.translate("local_xml_reader", u"Mais Informa\u00e7\u00f5es", None))
        self.lbl_forn.setText(QCoreApplication.translate("local_xml_reader", u": Fornecedor", None))
        self.lbl_cnpj.setText(QCoreApplication.translate("local_xml_reader", u": CNPJ", None))
        pass
    # retranslateUi

