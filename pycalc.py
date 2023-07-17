# To get started install PyQt6 with `python -m pip install pyqt6`
# Python version ^3.6.1
# This project was built with help from a tutorial, found here: https://realpython.com/python-pyqt-gui-calculator/#creating-a-calculator-app-with-python-and-pyqt
# Note: This is a beginner project meant to assist with basic understanding of MVC frameworks in Python

"""PyCalc is a basic calculator built with Python and PyQt using an MVC framework"""
import sys
from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

ERROR_MSG = "MATH ERROR"
WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40

# class Window inherits from QMainWindow
class PyCalcWindow(QMainWindow):
    """PyCalc's main window (view)"""

    # class initialization
    def __init__(self):
        # this is the app's main window
        super().__init__()
        # initializing window GUI
        self.setWindowTitle("PyCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]

        # iterates over 2 for loops to map the keyboard
        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)
        
        self.generalLayout.addLayout(buttonsLayout)

    # methods to show the text to the user, get the text from user inputs, and remove the text
    def setDisplayText(self, text):
            """Set the display's text."""
            self.display.setText(text)
            self.display.setFocus()

    def displayText(self):
            """Get the display's text."""
            return self.display.text()

    def clearDisplay(self):
            """Clear the display."""
            self.setDisplayText("")

def evaluateExpression(expression):
    """Evaluate an expression (model)"""
    # math based on user input, math error returns error message for user to see
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result

class PyCalc:
    """PyCalc's controller class"""

    # class initializers takes model and view as parameters
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        # evaluate the math based on user input
        result = self._evaluate(expression=self._view.displayText())
        # update display text
        self._view.setDisplayText(result)

    def _buildExpression(self, subExpression):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()

        # concatenating initial display v alue with all new values that are entered on the keyboard
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)
    
    # connect buttons with appropriate slots method in controller class
    def _connectSignalsAndSlots(self):
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=", "C"}:
                button.clicked.connect(
                    partial(self._buildExpression, keySymbol)
                )
            self._view.buttonMap["="].clicked.connect(self._calculateResult)
            self._view.display.returnPressed.connect(self._calculateResult)
            self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)

def main():
    """PyCalc's main function"""
    # creating a QApplication object
    pycalcApp = QApplication([])
    # creates instance of app window
    pycalcWindow = PyCalcWindow()
    # .show() displays GUI to user
    pycalcWindow.show()
    PyCalc(model=evaluateExpression, view=pycalcWindow)
    # running application event loop
    sys.exit(pycalcApp.exec())

if __name__ == "__main__":
    main()