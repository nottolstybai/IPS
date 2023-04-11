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
    "Parent": 2
  },
  {
    "ID": 2,
    "Text": "Требование 2",
    "Comment": "Комментарий 2",
    "Class": "B",
    "Parent": 1
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


def create_graph(data):
    graph = {}
    for req in data:
        id = req["ID"]
        category = req["Class"]
        parent = req["Parent"]
        if id not in graph:
            graph[id] = {"Children": [], "Category": category, "Parent": parent}
        if parent is not None:
            if parent not in graph:
                graph[parent] = {"Children": [], "Category": None, "Parent": None}
            graph[parent]["Children"].append(id)
        if id in graph and graph[id]["Category"] is None and graph[id]["Parent"] is None:
            graph[id]["Category"] = category
            graph[id]["Parent"] = parent
    return graph


def find_cycles(graph):
    G = nx.DiGraph()
    for node in graph:
        for child in graph[node]["Children"]:
            G.add_edge(node, child, CLASS=graph[node]["Category"])
    cycles = list(nx.simple_cycles(G))
    return cycles


def draw_graph(graph):
    G = nx.DiGraph()
    for node in graph:
        G.add_node(node)
        for child in graph[node]['Children']:
            G.add_edge(node, child)
    labels = {}
    colors = {}
    for node in graph:
        category = graph[node]['Category']
        # Создаем словарь меток id
        labels[node] = node
        # Если категория еще не имеет цвета, генерируем случайный цвет
        if category not in colors:
            colors[category] = (random.random(), random.random(), random.random())
    # Создаем список цветов для каждого узла в соответствии с его категорией
    node_colors = [colors[graph[node]['Category']] for node in graph]
    pos = nx.spring_layout(G)
    # Передаем словарь меток id в параметр labels
    nx.draw(G, pos=pos, with_labels=True, labels=labels, node_color=node_colors, cmap='jet')
    # Создаем подписи к категориям
    handles = []
    for category, color in colors.items():
        handles.append(plt.scatter([], [], color=color, label=category))
    plt.legend(handles=handles)
    plt.show()


def find_BNodes_to_notBnodes(graph):
    """функция для нахождения узлов класса B, ссылающихся на узлы класса F"""
    error_nodes = []
    for node in graph:
        if graph[node]["Category"] == "B":
            parent = graph[node]["Parent"]
            if parent is not None and graph[parent]["Category"] != "B":
                error_nodes.append(node)
    return error_nodes


if __name__ == '__main__':
    graph = create_graph(data)

    # выводим граф на экран
    print("Создан следующий граф:")
    print(graph)

    print("Найдены следующие циклы:")
    for cycle in find_cycles(graph):
        print(cycle)

    print("Ошибка наследования:")
    print(find_BNodes_to_notBnodes(graph))

    draw_graph(graph)
