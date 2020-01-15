###########################################################################################
# Bruce Rhoades - Desktop Calculator application built with PyQt which is a Python 
# binding for C++ libraries and dev tools that provide platform-independent abstractions
# for GUI functionality and other features
###########################################################################################

#!/usr/bin/env python3

# Filename: Calculator.py
import sys

import CalcFuncs as calcFuncs

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

__version__ = '0.1'
__author__ = 'Bruce Rhoades'


###########################################################################################
# Main Calculator Class
###########################################################################################
class CalculatorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set some main window's properties (vertical aligned Box)
        self.setWindowTitle('Calculator')
        self.setFixedSize(470, 520)
        self.generalLayout = QVBoxLayout()
        # Set the central widget to be the parent for the rest of the application
        # Orient the Main UI vertically (QVBoxLayout for generalLayout)
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self._centralWidget)
        # Create the display and the buttons
        self._createDisplay()
        self._createButtonLabels()
        self._createButtons()

        # Used to hold the operands of the caclulator
        self._operands = []

        # Used to hold the currently selected operation
        self._operation = None

        # Helper variables to indicate when an operation has been selected,
        # when the result has been computed and the current operand count
        self.operationSet = False
        self.resultSet = False
        self.operandCt = 0

    ###########################################################################################
    # Creates the top 2 components on the display: 
    # self.display is for the top (label) component showing the calculation expression
    # self.display two for displaying the operands and the result 
    ###########################################################################################
    def _createDisplay(self):
        # Create the label to display calculation expression
        self.display = QLabel()
        self.display.hasFrame = False
        # Set height, font, alignment
        self.display.setFixedHeight(50)
        self.display.setFont(QFont('Arial', 16))
        self.display.setAlignment(Qt.AlignRight)
        # Add the display to the general layout
        self.generalLayout.addWidget(self.display)

        # Create the component to display the operands and the result
        self.display2 = QLineEdit()
        # Set height, font, alignment, read only
        self.display2.setFixedHeight(70)
        self.display2.setFont(QFont('Arial', 24))
        self.display2.setAlignment(Qt.AlignRight)
        self.display2.setReadOnly(True)
        # Add the display to the general layout
        self.generalLayout.addWidget(self.display2)

    ###########################################################################################
    # Function to set the orientation order of the buttons on the calculator as well as the
    # labels for the buttons and lists of function references to be used when user selects
    # the buttons
    ###########################################################################################
    def _createButtonLabels(self):
        self.buttonLabels = [[['7', [self.displayTxt]], ['8', [self.displayTxt]], ['9', [self.displayTxt]], ['/', [self.setOperation, calcFuncs.CalcFuncs.divide]], ['C', [self.clearDisplay]]], 
                             [['4', [self.displayTxt]], ['5', [self.displayTxt]], ['6', [self.displayTxt]], ['*', [self.setOperation, calcFuncs.CalcFuncs.multiply]], ['EX', [self.setOperation, calcFuncs.CalcFuncs.exp]]],
                             [['1', [self.displayTxt]], ['2', [self.displayTxt]], ['3', [self.displayTxt]], ['-', [self.setOperation, calcFuncs.CalcFuncs.subtract]], ['SR', [self.setOperation, calcFuncs.CalcFuncs.sqareRoot, self.doCalc]]],
                             [['0', [self.displayTxt]], ['00', [self.displayTxt]], ['.', [self.displayTxt]], ['+', [self.setOperation, calcFuncs.CalcFuncs.add]], ['=', [self.doCalc]]]]

    
    ###########################################################################################
    # Method to create a dictionary of buttons (key) to reference the list of functions 
    # corresponding to the buttons (value). Buttons are created and positioned relative to their
    # positioning in the buttonLabels list. 
    ###########################################################################################
    def _createButtons(self):
            self.buttons ={}
            buttonsLayout = QGridLayout()

            for row in range(0, len(self.buttonLabels)):
                row_info = self.buttonLabels[row]
                for col in range(0, len(row_info)):
                    # create a button with label from buttonLabels
                    btn_info = self.buttonLabels[row][col]
                    calc_btn = QPushButton(btn_info[0])
                    calc_btn.setFixedSize(80,80)

                    # create a button click handler for the button, set the list of fn refernces as
                    # the value to the dictionary referenced by the button as the key
                    calc_btn.clicked.connect(self.onCalcBtnClick)
                    self.buttons[calc_btn] = btn_info[1]

                    # add the button to the layout
                    buttonsLayout.addWidget(calc_btn, row, col)
                    self.generalLayout.addLayout(buttonsLayout)

    ###########################################################################################
    # Button click handler for all the buttons on the calculator.
    ###########################################################################################
    def onCalcBtnClick(self):
        # Get the reference to the button that was clicked, as well as the list 
        # of related functions
        btn = self.sender()
        btnFuncs = self.buttons[btn]
        btnFunc1 = btnFuncs[0]
        btnFuncLen = len(btnFuncs)
        if(btnFuncLen == 1):
            # simply execute the one fn if we are computing the result or clearing the calculator
            if(btn.text() == '=') or (btn.text() == 'C'):
                btnFunc1()
            else:
                # pass the button text to display the data on the two ui controls
               btnFunc1(btn.text())
        elif(btnFuncLen == 2):
            # computational button with 2 operands selected. Display the operator accordingly and
            # set the operation to be computed later (see self.setOperation())
            self.displayTxt(btn.text(), False)
            btnFunc1(btnFuncs[1])
        else:
            # computational button with 1 operand selected (i.e., square root)
            # do nothing if a second operand or another operation is selected
            displayText = self.display.text()
            if((self.operandCt > 1) or (displayText[-1] in ['+','-','*','/','X','R'])):
                return
                
            # set the operation to be conducted, add the operand and then perform the calculation
            btnFunc1(btnFuncs[1])
            self._operands.append(float(self.display2.text()))
            btnFuncs[2](False)
    
    ###########################################################################################
    # Set the currently selected operation
    ###########################################################################################
    def setOperation(self, operation):
        if(self.operandCt < 2):
            self._operation = operation
            self.operationSet = True
    
    ###########################################################################################
    # Function to display text in both the label (display) and the line edit fields (display2)
    #
    # display - to display the operation expression
    # display2 - to display the individual operands and the result
    ###########################################################################################
    def displayTxt(self, text, isOperand=True):
        if(isOperand == False):
            self.operandCt += 1
            displayText = self.display.text()
            # do not accept more than one operator or consecutive operators
            if((self.operandCt > 1) or (displayText[-1] in ['+','-','*','/','X','R'])):
                return
        elif(text == '.'):
            # no more than one decimal allowed per operator
            cur_text2 = self.display2.text()
            if(cur_text2.find('.') >= 0):
                return

        # special logic for when the result has been computed
        if(self.resultSet == True):
            strOperand = str(self._operands[0])
            # remove decimals if a whole number has been computed
            if((len(strOperand) > 1) and (strOperand[-1] == '0' and strOperand[-2] == '.')):
                    strOperand = strOperand[0:-2]
            self.display.setText(strOperand)
            if(text[-1] not in ['+','-','*','/','X','R']):
                # Do not display operators in lower edit control
                cur_text2 = self.display2.text()
                self.display2.setText(cur_text2 + text)
                # remove operand as result becomes new first operand
                if(len(self._operands) > 0):
                    self._operands.pop(0)

        # Update the text in the upper label
        cur_text = self.display.text()
        self.display.setText(cur_text + text)

        # If we have just commputed the result we are done
        if(self.resultSet == True):
            self.resultSet = False
            return

        if(isOperand == True):
            if(self.operationSet == True):
                # clear the lower edit component if we have just set the operation
                # as we need to update it with the next operand
                self.display2.setText('')
                self.operationSet = False

            cur_text2 = self.display2.text()
            self.display2.setText(cur_text2 + text)
        else:
            # we have an operator, so now safe to update with the entered operand
            self._operands.append(float(self.display2.text()))
         
    ###########################################################################################
    # Function to set up and perform the calculation
    ###########################################################################################
    def doCalc(self, appendOperand=True):
        # Add the second operand if there is one
        if(appendOperand == True):
            self._operands.append(float(self.display2.text()))

        if(self._operation != None) and (len(self._operands) > 0):
            # invoke the operation if we have one and enough operands
            result = self._operation(self._operands)
            self.resultSet = True
            strResult = str(result)
            # remove the decimal for results that have whole numbers
            if((len(strResult) > 1) and (strResult[-1] == '0' and strResult[-2] == '.')):
                    strResult = strResult[0:-2]

            self.display2.setText(strResult)
            # store the result into the first operand for the next operation
            self._operands[0] = result
            self.operandCt = 0
            # remove the second operand
            if(len(self._operands) > 1):
                self._operands.pop(1)

    ###########################################################################################
    # Method to clear the display controls and reset related variables
    ###########################################################################################
    def clearDisplay(self):
        #Clear the display.
        self.display.setText('')
        self.display2.setText('')
        self._operands.clear()
        self._operation = None
        self.resultSet = False
        self.operandCt = 0

def main():
    # Create an instance of QApplication
    pycalc = QApplication(sys.argv)
    # Show the calculator's GUI
    view = CalculatorUI()
    view.show()
    # Execute the calculator's main event loop
    sys.exit(pycalc.exec_())

if __name__ == '__main__':
    main()