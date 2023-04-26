import json
import random

import matplotlib.pyplot as plt
import networkx as nx


class Requirement:
    def __init__(self, id, category, parent):
        self.id = id
        self.category = category
        self.parent = parent
        self.tests = []
        self.children = []

    def add_test(self, test_case):
        self.tests.append(test_case)

    def has_children(self):
        return len(self.children) > 0

    def __str__(self):
        return f"Requirement(id={self.id}, category={self.category}, parent={self.parent}, " \
               f"tests={self.tests}, children={self.children})"

    def __repr__(self):
        return f"Requirement(id={self.id}, category={self.category}, parent={self.parent}, " \
               f"tests={self.tests}, children={self.children})"


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        """Добавляет требование в граф"""
        if node.id not in self.nodes:
            self.nodes[node.id] = node

    def add_edge(self, parent, child):
        if parent not in self.nodes:
            self.add_node(Requirement(parent, None, None))
        if child not in self.nodes:
            self.add_node(Requirement(child, None, None))
        self.nodes[parent].children.append(child)

    def create_from_data(self, data: list):
        """Метод для создания графа из данных в виде словаря содержащих требования"""
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
        """метод для нахождения узлов класса B, не ссылающихся на узлы класса B"""
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

    def check_test_cases(self):
        """метод для нахождения требований, не покрытых тест кейсами"""
        incorrect_req = []
        for req_id, req in self.nodes.items():
            if not req.has_children():
                has_empty_case = any(not (case.test_steps and case.expected_results) for case in req.tests)
                if not req.tests or has_empty_case:
                    incorrect_req.append(req_id)
        return incorrect_req

    def draw_graph(self):
        """метод для визуализации графа с разными цветами для разных категорий"""
        G = nx.DiGraph()
        labels = {}
        colors = {}
        for node in self.nodes:
            req = self.nodes[node]
            category = req.category
            labels[node] = node
            if category not in colors:
                colors[category] = (random.random(), random.random(), random.random())
            G.add_node(node)
            for child in req.children:
                G.add_edge(node, child)
        node_colors = [colors[self.nodes[node].category] for node in self.nodes]
        pos = nx.spring_layout(G, seed=42)
        sorted_pos = dict(sorted(pos.items()))
        nx.draw(G, pos=sorted_pos, with_labels=True, labels=labels, node_color=node_colors, cmap='jet')
        handles = [plt.scatter([], [], color=color, label=category) for category, color in colors.items()]
        plt.legend(handles=handles)
        plt.show()

    def __str__(self):
        return f"Graph(nodes={self.nodes})"

    def __repr__(self):
        return f"Graph({len(self.nodes)} nodes)"
