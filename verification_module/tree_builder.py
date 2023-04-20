import json
import random

import matplotlib.pyplot as plt
import networkx as nx

data = json.loads("""
[
  {
    "ID": 1,
    "Text": "Требование 1",
    "Comment": "Комментарий 1",
    "Class": "F",
    "Parent": null
  },
  {
    "ID": 2,
    "Text": "Требование 2",
    "Comment": "Комментарий 2",
    "Class": "B",
    "Parent": 4
  },
  {
    "ID": 3,
    "Text": "Требование 3",
    "Comment": null,
    "Class": "F",
    "Parent": 2
  },
  {
    "ID": 4,
    "Text": "Требование 4",
    "Comment": null,
    "Class": "F",
    "Parent": 3
  }
]
""")


class Requirement:
    def __init__(self, id, category, parent):
        self.id = id
        self.category = category
        self.parent = parent
        self.tests = []
        self.children = []

    def add_test(self, test_case):
        self.tests.append(test_case)

    def __str__(self):
        return f"Requirement(id={self.id}, category={self.category}, parent={self.parent}, tests={self.tests})"

    def __repr__(self):
        return f"Requirement(id={self.id}, category={self.category}, parent={self.parent}, tests={self.tests})"


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        if node.id not in self.nodes:
            self.nodes[node.id] = node

    def add_edge(self, parent, child):
        if parent not in self.nodes:
            self.add_node(Requirement(parent, None, None))
        if child not in self.nodes:
            self.add_node(Requirement(child, None, None))
        self.nodes[parent].children.append(child)

    def create_from_data(self, data):
        for req in data:
            id = req["ID"]
            category = req["Class"]
            parent = req["Parent"]
            self.add_node(Requirement(id, category, parent))
            if parent is not None:
                self.add_edge(parent, id)
            if id in self.nodes and self.nodes[id].category is None and self.nodes[id].parent is None:
                self.nodes[id].category = category
                self.nodes[id].parent = parent
        return self

    def find_BNodes_to_notBnodes(self):
        """метод для нахождения узлов класса B, ссылающихся на узлы класса F"""
        error_nodes = []
        for node in self.nodes:
            if self.nodes[node].category == "B":
                parent = self.nodes[node].parent
                if parent is not None and self.nodes[parent].category != "B":
                    error_nodes.append(node)
        return error_nodes

    def find_alone_nodes(self):
        """метод для нахождения одиночных узлов"""
        error_nodes = []
        for node in self.nodes:
            if len(self.nodes[node].children) == 0 and self.nodes[node].parent is None:
                error_nodes.append(node)
        return error_nodes

    def find_cycles(self):
        """метод для нахождения циклов в графе"""
        G = nx.DiGraph()
        for node in self.nodes:
            for child in self.nodes[node].children:
                G.add_edge(node, child, CLASS=self.nodes[node].category)
        cycles = list(nx.simple_cycles(G))
        return cycles

    def draw_graph(self):
        """метод для визуализации графа с разными цветами для разных категорий"""
        G = nx.DiGraph()
        labels = {}
        colors = {}
        for node in self.nodes:
            category = self.nodes[node].category
            labels[node] = node
            if category not in colors:
                colors[category] = (random.random(), random.random(), random.random())
            G.add_node(node)
        for node in self.nodes:
            for child in self.nodes[node].children:
                G.add_edge(node, child)
        node_colors = [colors[self.nodes[node].category] for node in self.nodes]
        pos = nx.spring_layout(G, seed=42)  # добавить атрибут seed
        sorted_pos = dict(sorted(pos.items()))  # отсортировать словарь pos по ключам
        nx.draw(G, pos=sorted_pos, with_labels=True, labels=labels, node_color=node_colors, cmap='jet')
        handles = []
        for category, color in colors.items():
            handles.append(plt.scatter([], [], color=color, label=category))
        plt.legend(handles=handles)
        plt.show()

    def __str__(self):
        return f"Graph(nodes={self.nodes})"

    def __repr__(self):
        return f"Graph({len(self.nodes)} nodes)"


if __name__ == '__main__':
    graph1 = Graph()
    graph1.create_from_data(data)
    print(graph1)

    print(graph1.find_alone_nodes())
    print(graph1.find_cycles())
    print(graph1.find_BNodes_to_notBnodes())
    graph1.draw_graph()
