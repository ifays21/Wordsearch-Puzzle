import sys
import random
import string
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QColor, QBrush, QTextCursor
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QPushButton, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox, QMessageBox, \
    QTextEdit, QTableWidget, QProgressBar, QAbstractScrollArea, \
    QAbstractItemView, QLCDNumber, QTableWidgetItem, QApplication, QLineEdit, QDialog

puzzlesize = 10
wordBoxChecked = False
rowBoxChecked = False
columnBoxChecked = False
diagonalBoxChecked = False

class StartMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.w = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Menu")

        buttonStart = QPushButton('Start')
        buttonStart.clicked.connect(self.onClickStart)

        buttonQuit = QPushButton('Quit')
        buttonQuit.clicked.connect(self.onClickQuit)

        menuLabel = QLabel("Please input size of puzzle (default: 10)")

        self.sizevalue = QLineEdit(self)
        self.sizevalue.setAlignment(Qt.AlignCenter) 

        buttonBox = QHBoxLayout()
        buttonBox.addWidget(buttonStart)
        buttonBox.addWidget(buttonQuit)

        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(menuLabel,1, 0)
        grid.addWidget(self.sizevalue, 4, 0)
        grid.addLayout(buttonBox, 5, 0)

        self.show()

    def getTextValue(self):
        global puzzlesize
        puzzlesize = self.sizevalue.text()
        print(puzzlesize)

    def onClickStart(self):
        self.getTextValue()
        if int(puzzlesize) >= 10:
            if self.w is None:
                self.w = Puzzle()
            self.w.show()
            self.close()
        else: 
            self.errormessage()

    def errormessage(self):
        alertmsg = QMessageBox(self)
        alertmsg.setWindowTitle("Error!")
        alertmsg.setText("Please input size of 10 or more!")
        alertmsg.exec()
        okBtn = QMessageBox.Ok
    
    def onClickQuit(self, event):
        closing = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?', 
        QMessageBox.Yes  | QMessageBox.No, QMessageBox.No)

        if closing == QMessageBox.Yes:
            print('Window Closed')
            sys.exit()


class Puzzle(QWidget):
    def __init__(self):
        super().__init__()
        self.wordBank = ""
        self.wordBankSplit = []
        self.wordSelected = ""
        self.xVisited = []
        self.yVisited = []
        self.inRow = 0
        self.wordsCompleted = []
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Word Search Puzzle")

        self.wordBankbox = QTextEdit()
        self.tableWidget = QTableWidget()

       # self.createTable()
        self.createWordBank()
        self.mouseTracking()
        
        buttonClear = QPushButton('Clear', self)
        buttonClear.setToolTip('This clears your word selection.')
        buttonClear.clicked.connect(self.onClickClear)

        buttonQuit = QPushButton('Quit', self)
        buttonQuit.setToolTip('This button will quit your game. You will lose all progress.')
        buttonQuit.clicked.connect(self.onClickQuit)

        menu = QVBoxLayout()
       # menu.addWidget(self.wordBank)
        menu.addWidget(buttonClear)
        menu.addWidget(buttonQuit)

        self.grid = QGridLayout()
        self.grid.addLayout(menu, 0 ,1)
        self.grid.addWidget(self.tableWidget, 0, 0)

        self.setLayout(self.grid)

        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.show()

    #def createTable(self):

    def createWordBank(self):
        self.wordBankSplit = self.wordBank.split()
        self.wordBankSplit.sort()
        for x in self.wordBankSplit:
            self.wordBankbox.append(x)
        self.wordBankbox.setReadOnly(True)
        self.wordBankbox.setMaximumWidth(120)
        font = QFont()
        font.setFamily('Arial')
        self.wordBankbox.setFont(font)
        self.wordBankbox.moveCursor(QTextCursor.Start)

    def strikeWord(self, word):
        newWord = ""
        for x in word:
            newWord += x + '\u0336'
        self.wordBankSplit = [newWord if i == word else i for i in self.wordBankSplit]
        self.wordBankbox.setText("")
        for x in self.wordBankSplit:
            self.wordBankbox.append(x)
        self.wordBankbox.show()
        self.wordBankbox.moveCursor(QTextCursor.Start)

    def mouseTracking(self):
        self.currentHover = [0, 0]
        self.tableWidget.setMouseTracking(True)
        self.tableWidget.cellEntered.connect(self.cellHover)

    def cellHover(self, row, column):
        item = self.tableWidget.item(row, column)
        oldItem = self.tableWidget.item(self.currentHover[0], self.currentHover[1])
        mouseTracker1 = True
        mouseTracker2 = True
        for x in range(len(self.xVisited)):
            if self.xVisited[x] == row and self.yVisited[x] == column:
                mouseTracker1 = False
            if self.currentHover[0] == self.xVisited[x] and self.currentHover[1] == self.yVisited[x]:
                mouseTracker2 = False
        if mouseTracker1:
            if self.currentHover != [row, column]:
                if item.text().islower():
                    item.setBackground(QBrush(QColor('yellow')))
                if oldItem.text().islower() and mouseTracker2:
                    oldItem.setBackground(QBrush(QColor('white')))
        elif mouseTracker2:
            oldItem.setBackground(QBrush(QColor('white')))
        self.currentHover = [row, column]

    def onClickLetter(self):
        self.wordSelected = ""
        wordBankSplitOriginal = self.wordBank.split()
        selectionTracker = True
        selectionCorrectness = 0
        word = ""
        listX = []
        listY = []

        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            if self.tableWidget.item(currentQTableWidgetItem.row(), currentQTableWidgetItem.column()).text().isupper():
                letter = self.tableWidget.item(currentQTableWidgetItem.row(),
                                               currentQTableWidgetItem.column()).text().lower()
                self.tableWidget.setItem(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(),
                                         QTableWidgetItem(letter))
                self.tableWidget.clearSelection()
            else:
                for currentQTableWidgetItem in self.tableWidget.selectedItems():
                    for x in range(0, len(self.xVisited)):
                        if currentQTableWidgetItem.row() == self.xVisited[x] and currentQTableWidgetItem.column() == \
                                self.yVisited[x]:
                            selectionTracker = False
                    if selectionTracker:
                        letter = self.tableWidget.item(currentQTableWidgetItem.row(),
                                                       currentQTableWidgetItem.column()).text().upper()
                        self.tableWidget.setItem(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(),
                                                 QTableWidgetItem(letter))
                for currentQTableWidgetItem in self.tableWidget.selectedItems():
                    if selectionTracker:
                        self.tableWidget.item(currentQTableWidgetItem.row(),
                                              currentQTableWidgetItem.column()).setBackground(QColor(216, 191, 216))
                for currentQTableWidgetItem in self.tableWidget.selectedItems():
                    if selectionTracker:
                        self.tableWidget.item(currentQTableWidgetItem.row(),
                                              currentQTableWidgetItem.column()).setTextAlignment(
                            Qt.AlignCenter)
                    self.tableWidget.clearSelection()

        for x in range(0, puzzlesize):
            for y in range(0, puzzlesize):
                if self.tableWidget.item(x, y).text().isupper():
                    self.wordSelected += self.tableWidget.item(x, y).text()
                    listX.append(x)
                    listY.append(y)
        for x in wordBankSplitOriginal:
            if x == self.wordSelected.lower():
                selectionCorrectness += 1
                word = x
        if selectionCorrectness == 1:  # Makes sure the word is in a row
            for i in range(1, len(listY)):
                if listY[i - 1] == listY[i] - 1 and listX[i - 1] == listX[i]:
                    self.inRow += 1
                if self.inRow == len(listY) - 1:
                    selectionCorrectness += 1
                    self.inRow = 0
        if selectionCorrectness == 1:  # Makes sure the word is in a single column
            for i in range(1, len(listY)):
                if listX[i - 1] == listX[i] - 1 and listY[i - 1] == listY[i]:
                    self.inRow += 1
                if self.inRow == len(listY) - 1:
                    selectionCorrectness += 1
                    self.inRow = 0
        if selectionCorrectness == 1:  # Makes sure the word is in a forward diagonal
            for i in range(1, len(listY)):
                if listX[i - 1] == listX[i] - 1 and listY[i - 1] == listY[i] - 1:
                    self.inRow += 1
                if self.inRow == len(listY) - 1:
                    selectionCorrectness += 1
                    self.inRow = 0
        if selectionCorrectness == 1:  # Makes sure the word is in a backward diagonal
            for i in range(1, len(listY)):
                if listX[i - 1] == listX[i] - 1 and listY[i - 1] == listY[i] + 1:
                    self.inRow += 1
                if self.inRow == len(listY) - 1:
                    selectionCorrectness += 1
                    self.inRow = 0

        if selectionCorrectness == 2:
            wordIndex = self.wordSelected.find(word)
            self.progressValue += 1
            self.setProgressBar()
            self.strikeWord(word)
            self.wordsCompleted.append(word)
            for i in range(wordIndex, wordIndex + len(word)):
                letterI = self.tableWidget.item(listX[i], listY[i]).text().lower()
                self.tableWidget.setItem(listX[i], listY[i], QTableWidgetItem(letterI))
            for i in range(wordIndex, wordIndex + len(word)):
                self.tableWidget.item(listX[i], listY[i]).setBackground(QColor(144, 238, 144))
                self.xVisited.append(listX[i])
                self.yVisited.append(listY[i])
            for i in range(wordIndex, wordIndex + len(word)):
                self.tableWidget.item(listX[i], listY[i]).setTextAlignment(Qt.AlignCenter)

    def onClickClear(self):
        """Clear word selection on button click."""
        self.wordSelected = ""
        for x in range(0, puzzlesize):
            for y in range(0, puzzlesize):
                if self.tableWidget.item(x, y).text().isupper():
                    letterI = self.tableWidget.item(x, y).text().lower()
                    self.tableWidget.setItem(x, y, QTableWidgetItem(letterI))
                    self.tableWidget.item(x, y).setTextAlignment(Qt.AlignCenter)

    def onClickQuit(self):
        closing = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?', 
        QMessageBox.Yes  | QMessageBox.No, QMessageBox.No)

        if closing == QMessageBox.Yes:
            print('Window Closed')
            sys.exit()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = StartMenu()
    main.show()

    sys.exit(app.exec())