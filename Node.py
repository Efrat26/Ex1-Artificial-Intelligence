#Efrat Sofer 304855125


class Node:
    def __init__(self):
        visited = 0
        state = ''
        parent = None
    def setVisited(self, value):
        self.visited = value
    def setState(self, s):
        self.state = s
    def setParent(self, p):
        self.parent = p