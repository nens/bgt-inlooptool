# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 16:32:58 2026

@author: ruben.vanderzaag
"""

import os
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import QRegExp
from qgis.PyQt.QtGui import QRegExpValidator

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "PopUp_user_dialog.ui")
)

class PopUpUserDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Track clicked button
        self.choice = "later"  # default if closed with X

        self.pushButtonYes.clicked.connect(self.on_yes)
        self.pushButtonNo.clicked.connect(self.on_no)
        self.pushButtonLater.clicked.connect(self.on_later)

        # Disable Yes initially
        self.pushButtonYes.setEnabled(False)

        # Email validator
        email_regex = QRegExp(r"[^@]+@[^@]+\.[^@]+")
        self.inputMail.setValidator(QRegExpValidator(email_regex))

        # Connect validation
        self.inputMail.textChanged.connect(self.validate)
        self.inputOrg.textChanged.connect(self.validate)
    
    def on_yes(self):
        self.choice = "yes"
        self.accept()

    def on_no(self):
        self.choice = "no"
        self.accept()

    def on_later(self):
        self.choice = "later"
        self.accept()

    
    def validate(self):
        email_ok = self.inputMail.hasAcceptableInput()
        org_ok = len(self.inputOrg.text().strip()) > 0
        self.pushButtonYes.setEnabled(email_ok and org_ok)