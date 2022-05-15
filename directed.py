from turtle import update
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets
import networkx as nx
from GoalPage import GoalPage

class Canvas(FigureCanvas):
    
    def __init__(self, parent):
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure) 
        super().__init__(self.figure)
        self.setParent(parent)

        self.G= nx.DiGraph()

        print(self.G.graph)
        pos = nx.spring_layout(self.G)

        nx.draw(self.G , pos=pos, with_labels=True)
        

    def updateGraph(self,edgeFrom,edgeTo,cost):
        if cost ==0:
            self.figure.clf()
            self.G.add_edge(edgeFrom,edgeTo)

            print(self.G.graph)
            pos = nx.spring_layout(self.G)

            nx.draw(self.G , pos=pos, with_labels=True)

            print(self.G[edgeFrom])

            print("Updating Graph")
        else:
            self.figure.clf()
            self.G.add_edge(edgeFrom,edgeTo,weight=cost)

            pos = nx.spring_layout(self.G)

            nx.draw(self.G , pos=pos, with_labels=True)
            nx.draw_networkx_edge_labels(self.G,pos , edge_labels=nx.get_edge_attributes(self.G,'weight'))

            
    
    def AddHeuristicInNode(self,nodeName,heuristic):
        
        if self.G.has_node(nodeName):
            self.figure.clf()
            self.G.nodes[nodeName]['heuristic']=heuristic
            self.G = nx.relabel_nodes(self.G, {nodeName:str(nodeName) +" h=" +str(heuristic)})

            pos = nx.spring_layout(self.G)
            nx.draw(self.G , pos=pos, with_labels=True)
            nx.draw_networkx_edge_labels(self.G,pos , edge_labels=nx.get_edge_attributes(self.G,'weight'))

            return 1
        else:
            return 0

        


class directedGraphWindow(QWidget):
    def __init__(self,withCost,withHeuristic):
        super().__init__()
        self.resize(1600, 800)
        self.chart = Canvas(self)
        self.chart.setGeometry(50,50,1100,700)
        self.withCost = withCost
        self.withHeuristic = withHeuristic
        self.initUI()

    def AddEdge(self):
        if self.edgeFrom.text() and self.edgeTo.text():
            if self.withCost:
                if self.incost.text().isdigit():
                    self.chart.updateGraph(self.edgeFrom.text(),self.edgeTo.text(),self.incost.text())
                else: self.error.setText("Cost must be integer")
            else:
                self.chart.updateGraph(self.edgeFrom.text(),self.edgeTo.text(),0)
            self.chart.draw_idle()
        else:
            self.error.setText("From and To nodes are required")

    
    def AddHeuristic(self):
        self.addEdge.setEnabled(False)
        if self.inHeuristic.text() and self.nodeName.text():
            if self.inHeuristic.text().isdigit():
                res=self.chart.AddHeuristicInNode(self.nodeName.text(),self.inHeuristic.text())
                self.chart.draw_idle()

                if(res==0):
                    self.error.setText("Node not found")
                else: self.error.setText("")
            else: self.error.setText("Heuristic must be an integer")
        else:
            self.error.setText("Node Name and Heuristic is required")

    def NextPage(self):
        self.dWindow = GoalPage(self.chart.G)
        self.dWindow.show()

    def initUI(self):

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(1200, 50, 400, 50)
        self.label.setText("Add Edge:")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(1200, 100, 400, 50)
        self.label.setText("From:")
        
        self.edgeFrom = QtWidgets.QLineEdit(self)
        self.edgeFrom.setGeometry(1200, 150, 300, 50)
        self.edgeFrom.setPlaceholderText("From")
        self.edgeFrom.setObjectName("edgeFrom")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(1200, 200, 400, 50)
        self.label.setText("To:")

        self.edgeTo = QtWidgets.QLineEdit(self)
        self.edgeTo.setGeometry(1200, 250, 300, 50)
        self.edgeTo.setObjectName("edgeTo")

        self.addEdge = QtWidgets.QPushButton(self)
        self.addEdge.setGeometry(1200, 400, 200, 50)
        self.addEdge.setObjectName("addBtn")
        self.addEdge.setText("Add edge")
        self.addEdge.clicked.connect(self.AddEdge)

        if(self.withCost):
            self.incost = QtWidgets.QLineEdit(self)
            self.incost.setGeometry(1200, 300, 300, 50)
            self.incost.setPlaceholderText("Cost")
            self.incost.setObjectName("incost")

        if self.withHeuristic:
            self.label = QtWidgets.QLabel(self)
            self.label.setGeometry(1200, 450, 400, 50)
            self.label.setText("Add Heuristic:")
            
            self.nodeName = QtWidgets.QLineEdit(self)
            self.nodeName.setGeometry(1200, 500, 300, 50)
            self.nodeName.setPlaceholderText("Node Name")
            self.nodeName.setObjectName("nodeName")

            self.inHeuristic = QtWidgets.QLineEdit(self)
            self.inHeuristic.setGeometry(1200, 550, 100, 50)
            self.inHeuristic.setPlaceholderText("Heuristic")
            self.inHeuristic.setObjectName("inHeuristic")

            self.addHeuristic = QtWidgets.QPushButton(self)
            self.addHeuristic.setGeometry(1200, 650, 200, 50)
            self.addHeuristic.setObjectName("addBtn")
            self.addHeuristic.setText("Add Heuristic")
            self.addHeuristic.clicked.connect(self.AddHeuristic)

        self.nextPage = QtWidgets.QPushButton(self)
        self.nextPage.setGeometry(1200, 700, 200, 50)
        self.nextPage.setObjectName("nextPage")
        self.nextPage.setText("Next Page")
        self.nextPage.clicked.connect(self.NextPage)
        
        self.error = QtWidgets.QLabel(self)
        self.error.setStyleSheet("color: red;")
        self.error.setGeometry(1200, 750, 400, 50)

    

