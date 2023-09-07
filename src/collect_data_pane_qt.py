# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'collect_data_pane_qt_2.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_CollectDataPane(object):
    def setupUi(self, CollectDataPane):
        if not CollectDataPane.objectName():
            CollectDataPane.setObjectName(u"CollectDataPane")
        CollectDataPane.resize(320, 304)
        self.gridLayout = QGridLayout(CollectDataPane)
        self.gridLayout.setObjectName(u"gridLayout")
        self.notes_no_spin = QSpinBox(CollectDataPane)
        self.notes_no_spin.setObjectName(u"notes_no_spin")

        self.gridLayout.addWidget(self.notes_no_spin, 0, 0, 1, 1)

        self.notes_lbl = QLabel(CollectDataPane)
        self.notes_lbl.setObjectName(u"notes_lbl")

        self.gridLayout.addWidget(self.notes_lbl, 0, 1, 1, 1)

        self.establ_combo = QComboBox(CollectDataPane)
        self.establ_combo.setObjectName(u"establ_combo")

        self.gridLayout.addWidget(self.establ_combo, 1, 0, 1, 1)

        self.establ_lbl = QLabel(CollectDataPane)
        self.establ_lbl.setObjectName(u"establ_lbl")

        self.gridLayout.addWidget(self.establ_lbl, 1, 1, 1, 1)

        self.nat_op_entr = QLineEdit(CollectDataPane)
        self.nat_op_entr.setObjectName(u"nat_op_entr")

        self.gridLayout.addWidget(self.nat_op_entr, 2, 0, 1, 1)

        self.nat_op_lbl = QLabel(CollectDataPane)
        self.nat_op_lbl.setObjectName(u"nat_op_lbl")

        self.gridLayout.addWidget(self.nat_op_lbl, 2, 1, 1, 1)

        self.cfop_combo = QComboBox(CollectDataPane)
        self.cfop_combo.setObjectName(u"cfop_combo")

        self.gridLayout.addWidget(self.cfop_combo, 3, 0, 1, 1)

        self.cfop_lbl = QLabel(CollectDataPane)
        self.cfop_lbl.setObjectName(u"cfop_lbl")

        self.gridLayout.addWidget(self.cfop_lbl, 3, 1, 1, 1)

        self.fato_gerador_edit = QDateEdit(CollectDataPane)
        self.fato_gerador_edit.setObjectName(u"fato_gerador_edit")
        self.fato_gerador_edit.setDate(QDate(2023, 1, 1))

        self.gridLayout.addWidget(self.fato_gerador_edit, 4, 0, 1, 1)

        self.fato_ger_lbl = QLabel(CollectDataPane)
        self.fato_ger_lbl.setObjectName(u"fato_ger_lbl")

        self.gridLayout.addWidget(self.fato_ger_lbl, 4, 1, 1, 1)

        self.nat_op_button = QPushButton(CollectDataPane)
        self.nat_op_button.setObjectName(u"nat_op_button")
        font = QFont()
        font.setPointSize(10)
        self.nat_op_button.setFont(font)

        self.gridLayout.addWidget(self.nat_op_button, 5, 0, 2, 1)

        self.query_data_btn = QPushButton(CollectDataPane)
        self.query_data_btn.setObjectName(u"query_data_btn")
        self.query_data_btn.setFont(font)

        self.gridLayout.addWidget(self.query_data_btn, 5, 1, 1, 1)

        self.collect_data_btn = QPushButton(CollectDataPane)
        self.collect_data_btn.setObjectName(u"collect_data_btn")
        self.collect_data_btn.setFont(font)

        self.gridLayout.addWidget(self.collect_data_btn, 6, 1, 1, 1)


        self.retranslateUi(CollectDataPane)

        QMetaObject.connectSlotsByName(CollectDataPane)
    # setupUi

    def retranslateUi(self, CollectDataPane):
        CollectDataPane.setWindowTitle(QCoreApplication.translate("CollectDataPane", u"Form", None))
        self.notes_lbl.setText(QCoreApplication.translate("CollectDataPane", u": N\u00b0 of Notes", None))
        self.establ_lbl.setText(QCoreApplication.translate("CollectDataPane", u":Establ", None))
        self.nat_op_entr.setText(QCoreApplication.translate("CollectDataPane", u"S99.44", None))
        self.nat_op_lbl.setText(QCoreApplication.translate("CollectDataPane", u": Nat. Op", None))
        self.cfop_lbl.setText(QCoreApplication.translate("CollectDataPane", u":CFOP", None))
        self.fato_ger_lbl.setText(QCoreApplication.translate("CollectDataPane", u": Fato Gerador", None))
        self.nat_op_button.setText(QCoreApplication.translate("CollectDataPane", u"Mudar Nat. Op", None))
        self.query_data_btn.setText(QCoreApplication.translate("CollectDataPane", u"Pesquisar Notas", None))
        self.collect_data_btn.setText(QCoreApplication.translate("CollectDataPane", u"Coletar Dados", None))
    # retranslateUi

