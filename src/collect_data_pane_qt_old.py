# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'collect_data_pane_qt.ui'
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
        self.collect_data_btn = QPushButton(CollectDataPane)
        self.collect_data_btn.setObjectName(u"collect_data_btn")
        self.collect_data_btn.setGeometry(QRect(140, 240, 141, 23))
        self.nat_op_button = QPushButton(CollectDataPane)
        self.nat_op_button.setObjectName(u"nat_op_button")
        self.nat_op_button.setGeometry(QRect(30, 220, 91, 23))
        self.cfop_combo = QComboBox(CollectDataPane)
        self.cfop_combo.setObjectName(u"cfop_combo")
        self.cfop_combo.setGeometry(QRect(40, 130, 81, 22))
        self.establ_combo = QComboBox(CollectDataPane)
        self.establ_combo.setObjectName(u"establ_combo")
        self.establ_combo.setGeometry(QRect(40, 70, 81, 22))
        self.nat_op_entr = QLineEdit(CollectDataPane)
        self.nat_op_entr.setObjectName(u"nat_op_entr")
        self.nat_op_entr.setGeometry(QRect(40, 100, 81, 20))
        self.notes_no_spin = QSpinBox(CollectDataPane)
        self.notes_no_spin.setObjectName(u"notes_no_spin")
        self.notes_no_spin.setGeometry(QRect(50, 40, 71, 22))
        self.notes_lbl = QLabel(CollectDataPane)
        self.notes_lbl.setObjectName(u"notes_lbl")
        self.notes_lbl.setGeometry(QRect(140, 40, 71, 16))
        self.establ_lbl = QLabel(CollectDataPane)
        self.establ_lbl.setObjectName(u"establ_lbl")
        self.establ_lbl.setGeometry(QRect(140, 70, 71, 16))
        self.nat_op_lbl = QLabel(CollectDataPane)
        self.nat_op_lbl.setObjectName(u"nat_op_lbl")
        self.nat_op_lbl.setGeometry(QRect(140, 100, 71, 16))
        self.cfop_lbl = QLabel(CollectDataPane)
        self.cfop_lbl.setObjectName(u"cfop_lbl")
        self.cfop_lbl.setGeometry(QRect(140, 130, 71, 16))
        self.query_data_btn = QPushButton(CollectDataPane)
        self.query_data_btn.setObjectName(u"query_data_btn")
        self.query_data_btn.setGeometry(QRect(140, 210, 141, 23))
        self.fato_ger_lbl = QLabel(CollectDataPane)
        self.fato_ger_lbl.setObjectName(u"fato_ger_lbl")
        self.fato_ger_lbl.setGeometry(QRect(140, 170, 81, 16))
        self.fato_gerador_edit = QDateEdit(CollectDataPane)
        self.fato_gerador_edit.setObjectName(u"fato_gerador_edit")
        self.fato_gerador_edit.setGeometry(QRect(30, 170, 91, 22))
        self.fato_gerador_edit.setDate(QDate(2023, 1, 1))

        self.retranslateUi(CollectDataPane)

        QMetaObject.connectSlotsByName(CollectDataPane)
    # setupUi

    def retranslateUi(self, CollectDataPane):
        CollectDataPane.setWindowTitle(QCoreApplication.translate("CollectDataPane", u"Form", None))
        self.collect_data_btn.setText(QCoreApplication.translate("CollectDataPane", u"Collect Data From Fiscal!", None))
        self.nat_op_button.setText(QCoreApplication.translate("CollectDataPane", u"Change Nat. Op", None))
        self.nat_op_entr.setText(QCoreApplication.translate("CollectDataPane", u"S99.44", None))
        self.notes_lbl.setText(QCoreApplication.translate("CollectDataPane", u": N\u00b0 of Notes", None))
        self.establ_lbl.setText(QCoreApplication.translate("CollectDataPane", u":Establ", None))
        self.nat_op_lbl.setText(QCoreApplication.translate("CollectDataPane", u": Nat. Op", None))
        self.cfop_lbl.setText(QCoreApplication.translate("CollectDataPane", u":CFOP", None))
        self.query_data_btn.setText(QCoreApplication.translate("CollectDataPane", u"Query Data", None))
        self.fato_ger_lbl.setText(QCoreApplication.translate("CollectDataPane", u": Fato Gerador", None))
    # retranslateUi

