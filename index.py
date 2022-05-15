import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets,QtCore
from directed import directedGraphWindow 
from indirected import inDirectedGraphWindow

class firstWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.initUI()

    def dir(self):
        if self.heuristic.isChecked():
            self.cost.setChecked(True)
        self.dWindow = directedGraphWindow(self.cost.isChecked(),self.heuristic.isChecked())
        self.dWindow.show()
    
    def indir(self):
        
        if self.heuristic.isChecked():
            self.cost.setChecked(True)

        self.iWindow = inDirectedGraphWindow(self.cost.isChecked(),self.heuristic.isChecked())
        self.iWindow.show()

    def initUI(self):

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(300, 100, 200, 40)
        self.label.setObjectName("label")
        self.label.setText("Please Select an option")

        self.directedBtn = QtWidgets.QPushButton(self)
        self.directedBtn.setGeometry(175, 200, 200, 40)
        self.directedBtn.setText("Directed Graph")
        self.directedBtn.clicked.connect(self.dir)
        self.directedBtn.setObjectName("directedBtn")

        self.indirectedBtn = QtWidgets.QPushButton(self)
        self.indirectedBtn.setGeometry(425, 200, 200, 40)
        self.indirectedBtn.setText("Indirected Graph")
        self.indirectedBtn.clicked.connect(self.indir)
        self.indirectedBtn.setObjectName("indirectedBtn")

        self.cost = QtWidgets.QCheckBox(self)
        self.cost.setGeometry(175, 250, 100, 40)
        self.cost.setText("With cost")

        self.heuristic = QtWidgets.QCheckBox(self)
        self.heuristic.setGeometry(175, 300, 200, 40)
        self.heuristic.setText("With heuristic")


app = QApplication(sys.argv)
demo = firstWindow()
demo.show()
sys.exit(app.exec_())