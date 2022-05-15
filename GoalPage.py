from turtle import st, update
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets
import networkx as nx

class Canvas(FigureCanvas):
    
    def __init__(self, parent,myG,color_map):
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure) 
        super().__init__(self.figure)
        self.setParent(parent)
        self.color_map = color_map

        self.G= myG

        print(self.G.graph)
        pos = nx.spring_layout(self.G)

        nx.draw(self.G , pos=pos , node_color=self.color_map , with_labels=True)
        nx.draw_networkx_edge_labels(self.G,pos , edge_labels=nx.get_edge_attributes(self.G,'weight'))


    def updateGraph(self,start,goals):
        goals=goals.split(',')
        self.color_map=[]
        for node in self.G.nodes:
            nodeName = node.split(' ')
            print(nodeName[0] )
            if nodeName[0] == start:
                self.color_map.append('red')
            elif nodeName[0] in goals :
                self.color_map.append('green')
            else: 
                self.color_map.append('yellow') 
        
        return self.color_map

    def ColorPath(self,G,path):
        self.figure.clf()
        self.G = G
        edges = self.G.edges()
        
        for x,y in edges:
            self.G[x][y]['color']='black'
        for i in range(len(path)-1):
            j=i+1
            self.G[path[i]][path[j]]['color'] = 'yellow'
        
        colors = [self.G[u][v]['color'] for u,v in edges]
        pos = nx.spring_layout(self.G)
        nx.draw(self.G , pos=pos , node_color=self.color_map , with_labels=True)
        nx.draw_networkx_edges(self.G,pos, edgelist=G.edges() ,edge_color=colors)
        nx.draw_networkx_edge_labels(self.G,pos , edge_labels=nx.get_edge_attributes(self.G,'weight'))

        
class FinalPage(QWidget):
    def __init__(self,G,Algorithm,color_map,start,goals, maximumDepth):
        super().__init__()
        self.resize(1600, 800)
        self.chart = Canvas(self,G,color_map)
        self.chart.setGeometry(50,50,1500,700)
        self.Algorithm = Algorithm
        self.start = start
        self.goals= goals.split(",")
        print("goals List",self.goals)
        self.G=G
        if maximumDepth:
            self.maximumDepth = int(maximumDepth)
        

        self.UIinit()
        
    def bfs(self,graph, start, goal):
        visited =[]
        queue =[[start]]
        while queue:
            path =queue.pop(0)
            node = path[-1]
            if node in visited:
                continue
            visited.append(node)
            if node in goal:
                return path
            else:
                adjacent_nodes = graph.get(node,[])
                for node2 in adjacent_nodes:
                    new_path = path.copy()
                    new_path.append(node2)
                    queue.append(new_path)

    def dfs(self,graph,start,goal):
        visited =[]
        stack =[[start]]
        while stack:
            path =stack.pop()
            node = path[-1]
            if node in visited:
                continue
            visited.append(node)
            if node in goal:
                return path
            else:
                adjacent_nodes = graph.get(node,[])
                for node2 in adjacent_nodes:
                    new_path = path.copy()
                    new_path.append(node2)
                    stack.append(new_path)
    def path_cost(self,path):
        total_cost=0
        for (node,cost)in path:
            total_cost+=cost
        return total_cost , path[-1][0]

    def ucs (self,graph,start,goal):
        visited=[]
        queue=[[(start,0)]]
        path=[(start,0)]
        while queue:
            queue.sort(key=self.path_cost)
            path=queue.pop(0)
            node=path[-1][0]
            if node in visited:
                continue
            visited.append(node)
            if node in goal:
                return path
            else:
                adjacent_nodes=graph.get(node,[])
                for (node2,cost) in adjacent_nodes:
                    new_path=path.copy()
                    new_path.append((node2,cost))
                    queue.append(new_path)

    def DFS(self,currentNode,destination,graph,maxDepth,curList):
        curList.append(currentNode)
        if currentNode in destination:
            return True , curList
        if maxDepth<=0:
            self.path.append(curList)
            return False, curList
        for node in graph[currentNode]:
            (found , goalPath) = self.DFS(node,destination,graph,maxDepth-1,curList)
            if found:
                return True ,goalPath
            else:
                curList.pop()
        return False ,curList

    def iterativeDDFS(self,currentNode,destination,graph,maxDepth):
        for i in range(maxDepth):
            curList = []
            (found , goalPath) =self.DFS(currentNode,destination,graph,i,curList)
            if found:
                return True, goalPath
        return False, goalPath

    def path_f_cost(self,path):
        g_cost = 0
        for (node,cost) in path:
            g_cost += cost
        last_node = path[-1][0]
        h_cost = self.H_table[last_node]
        f_cost = g_cost + h_cost
        return f_cost, last_node


    def a_star_search(self,graph, start, goal):
        visited = []
        queue = [[(start,0)]]
        while queue:
            queue.sort(key= self.path_f_cost)
            path = queue.pop(0)
            node = path[-1][0]
            if node in visited:
                continue
            visited.append(node)
            if node in goal:
                return path
            else:
                adjacent_nodes = graph.get(node,[])
                for (node2, cost) in adjacent_nodes:
                    new_path = path.copy()
                    new_path.append((node2,cost))
                    queue.append(new_path)
    def path_h_cost(self,path):
        g_cost = 0
        for (node,cost) in path:
            g_cost += cost
        last_node = path[-1][0]
        h_cost = self.H_table[last_node]
        f_cost = g_cost + h_cost
        return h_cost, last_node


    def Greedy_Search(self,graph, start, goal):
        visited = []
        queue = [[(start,0)]]
        while queue:
            queue.sort(key= self.path_h_cost)
            path = queue.pop(0)
            node = path[-1][0]
            if node in visited:
                continue
            visited.append(node)
            if node in goal:
                return path
            else:
                adjacent_nodes = graph.get(node,[])
                for (node2, cost) in adjacent_nodes:
                    new_path = path.copy()
                    new_path.append((node2,cost))
                    queue.append(new_path)
    

    def UIinit(self):
        if self.Algorithm == 'Breadth First':
            graph = {k.split(' ')[0] :[] for k in self.G.nodes}
            
            for node in self.G.nodes:
                edgeList =[]
                for edge in self.G.edges(node):
                    to = edge[1].split(" ")
                    edgeList.append(to[0])
                graph[node.split(" ")[0]] = edgeList

            path=self.bfs(graph,self.start,self.goals)
            for i in range(len(path)):
                for n in self.G.nodes:
                    split = n.split(' ')
                    if(path[i]== split[0]) :
                        path[i] = n
                        continue
            print(path)
            
            self.chart.ColorPath(self.G,path)
            self.chart.draw_idle()
        
        elif self.Algorithm == 'Depth First':
            graph = {k.split(' ')[0] :[] for k in self.G.nodes}
            
            for node in self.G.nodes:
                edgeList =[]
                for edge in self.G.edges(node):
                    to = edge[1].split(" ")
                    edgeList.append(to[0])
                graph[node.split(" ")[0]] = edgeList

            path = self.dfs(graph,self.start,self.goals)
            for i in range(len(path)):
                for n in self.G.nodes:
                    split = n.split(' ')
                    if(path[i]== split[0]) :
                        path[i] = n
                        continue
            self.chart.ColorPath(self.G,path)
            self.chart.draw_idle()
        
        elif self.Algorithm == 'Uniform Cost':
            graph = {k:[] for k in self.G.nodes}
            # if indirected
            if self.G.is_directed():
                for u,v,c in self.G.edges.data('weight'):
                    graph[u].append((v,int(c)))
            else:
                for u,v,c in self.G.edges.data('weight'):
                    graph[u].append((v,int(c)))
                    graph[v].append((u,int(c)))

            print('my graph is')
            print(graph)
            path = []
            for u,v in self.ucs(graph,self.start,self.goals):
                path.append(u)
            self.chart.ColorPath(self.G,path)
            self.chart.draw_idle()
        
        elif self.Algorithm == 'A*':
            graph = {k.split(' ')[0] :[] for k in self.G.nodes}

            if self.G.is_directed():
                for u,v,c in self.G.edges.data('weight'):
                    u = u.split(" ")
                    v = v.split(" ")
                    graph[u[0]].append((v[0],int(c)))
            else:
                for u,v,c in self.G.edges.data('weight'):
                    u = u.split(" ")
                    
                    v = v.split(" ")
                    
                    graph[u[0]].append((v[0],int(c)))
                    graph[v[0]].append((u[0],int(c)))
                

            print('my graph is')
            print(graph)

            self.H_table = {}

            self.H_table = {}
            for u,v in self.G.nodes.data('heuristic'):
                u = u.split(" ")
                self.H_table[u[0]]=int(v)

            print(self.H_table)
            path = []
            for u,v in self.a_star_search(graph,self.start,self.goals):
                path.append(u)
            for i in range(len(path)):
                for n in self.G.nodes:
                    split = n.split(' ')
                    if(path[i]== split[0]) :
                        path[i] = n
                        continue
            print(path)
            self.chart.ColorPath(self.G,path)
            self.chart.draw_idle()
        
        elif self.Algorithm == 'Greedy':
            graph = {k.split(' ')[0] :[] for k in self.G.nodes}

            if self.G.is_directed():
                for u,v,c in self.G.edges.data('weight'):
                    u = u.split(" ")
                    v = v.split(" ")
                    graph[u[0]].append((v[0],int(c)))
            else:
                for u,v,c in self.G.edges.data('weight'):
                    u = u.split(" ")
                    
                    v = v.split(" ")
                    
                    graph[u[0]].append((v[0],int(c)))
                    graph[v[0]].append((u[0],int(c)))
                

            print('my graph is')
            print(graph)

            self.H_table = {}

            self.H_table = {}
            for u,v in self.G.nodes.data('heuristic'):
                u = u.split(" ")
                self.H_table[u[0]]=int(v)

            print(self.H_table)
            path = []
            for u,v in self.Greedy_Search(graph,self.start,self.goals):
                path.append(u)
            for i in range(len(path)):
                for n in self.G.nodes:
                    split = n.split(' ')
                    if(path[i]== split[0]) :
                        path[i] = n
                        continue

            self.chart.ColorPath(self.G,path)
            self.chart.draw_idle()
        elif self.Algorithm == 'Iterative Deepening':

            graph = {k.split(' ')[0] :[] for k in self.G.nodes}
            self.path = list()
    
            for node in self.G.nodes:
                edgeList =[]
                for edge in self.G.edges(node):
                    to = edge[1].split(" ")
                    edgeList.append(to[0])
                graph[node.split(" ")[0]] = edgeList

            (found , goalPath) = self.iterativeDDFS(self.start,self.goals,graph,self.maximumDepth)

            for i in range(len(goalPath)):
                for n in self.G.nodes:
                    split = n.split(' ')
                    if(goalPath[i]== split[0]) :
                        goalPath[i] = n
                        continue

            self.chart.ColorPath(self.G,goalPath)
            self.chart.draw_idle()



class GoalPage(QWidget):
    def __init__(self,G):
        super().__init__()
        self.resize(1600, 800)
        self.chart = Canvas(self,G,['yellow'])
        self.chart.setGeometry(50,50,1100,700)
        self.initUI()

    def RunAlgorithm(self):
        nodes = []
        for n in self.chart.G.nodes():
            nodes.append(n.split(" ")[0])
        if self.startState.text() in nodes and self.goalState.text() in nodes:
            cMap=self.chart.updateGraph(self.startState.text(),self.goalState.text())
            if self.maximumDepth.text():
                self.finalPage = FinalPage(self.chart.G ,self.selectAlgorithm.currentText(),cMap,self.startState.text(),self.goalState.text(),self.maximumDepth.text())
            else: self.finalPage = FinalPage(self.chart.G ,self.selectAlgorithm.currentText(),cMap,self.startState.text(),self.goalState.text(),0)
            self.finalPage.show()
        else:
            self.error.setText("Start node and/or goal node not found")

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(1200, 100, 400, 50)
        self.label.setText("Please Enter Start and Goal Nodes")
        
        self.startState = QtWidgets.QLineEdit(self)
        self.startState.setGeometry(1200, 150, 200, 50)
        self.startState.setPlaceholderText("Start Node")
        self.startState.setObjectName("startState")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(1200, 200, 400, 50)
        self.label.setText("You can input many goal nodes separated by (,)")

        self.goalState = QtWidgets.QLineEdit(self)
        self.goalState.setGeometry(1200, 250, 200, 50)
        self.goalState.setPlaceholderText("Goal Node(s)")
        self.goalState.setObjectName("goalState")

        self.selectAlgorithm = QtWidgets.QComboBox(self)
        self.selectAlgorithm.setGeometry(1200, 300, 200, 50)
        self.selectAlgorithm.addItems(['Depth First','Breadth First','Uniform Cost','Iterative Deepening','Greedy','A*'])

        # text field for max depth in iterative deepening
        self.maximumDepth = QtWidgets.QLineEdit(self)
        self.maximumDepth.setGeometry(1200, 350, 200, 50)
        self.maximumDepth.setPlaceholderText("Max Depth (only for IDDP)")
        self.maximumDepth.setObjectName("edgeFrom")

        self.runAlgorithm = QtWidgets.QPushButton(self)
        self.runAlgorithm.setGeometry(1200, 450, 200, 50)
        self.runAlgorithm.setObjectName("addBtn")
        self.runAlgorithm.setText("Run Algorithm")
        self.runAlgorithm.clicked.connect(self.RunAlgorithm)

        self.error = QtWidgets.QLabel(self)
        self.error.setStyleSheet("color: red;")
        self.error.setGeometry(1200, 550, 400, 50)

        