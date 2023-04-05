import json


class Node:
    def __init__(self, id, text, comment, class_):
        """Конструктор класса принимает id, text, comment и class узла"""
        self.id = id
        self.text = text
        self.comment = comment
        self.class_ = class_
        self.children = []

    def add_child(self, child):
        """Метод для добавления дочернего узла"""
        self.children.append(child)

    def print_info(self, level=0):
        """Метод для вывода информации об узле и его детях"""
        print("  " * level, end="")
        print(f"ID: {self.id}, Text: {self.text}, Class: {self.class_}")
        if self.comment:
            print("  " * level, end="")
            print(f"Comment: {self.comment}")
        for child in self.children:
            child.print_info(level + 1)


def parse_data(filename):
    with open(filename, "r") as f:
        """Считываем данные из файла и преобразуем их в список словарей"""
        data = json.load(f)

    nodes = {}

    for d in data:
        node = Node(d["ID"], d["Text"], d["Comment"], d["Class"])
        nodes[node.id] = node
    roots = []

    for d in data:
        # Если есть поле Parent и оно не равно null
        if d["Parent"] and d["Parent"] != "null":
            # Находим родительский узел по его id в словаре nodes
            parent = nodes[d["Parent"]]
            # Находим дочерний узел по его id в словаре nodes
            child = nodes[d["ID"]]
            # Добавляем дочерний узел к родительскому
            parent.add_child(child)
        else:
            # Иначе добавляем узел в список корневых узлов
            roots.append(nodes[d["ID"]])
    return roots