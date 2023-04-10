import json

import matplotlib.pyplot as plt
import networkx as nx

data = json.loads("""
[
  {
    "ID": 1,
    "Text": "Требование 1",
    "Comment": "Комментарий 1",
    "Class": "B",
    "Parent": 4
  },
  {
    "ID": 2,
    "Text": "Требование 2",
    "Comment": "Комментарий 2",
    "Class": "F",
    "Parent": 1
  },
  {
    "ID": 3,
    "Text": "Требование 3",
    "Comment": null,
    "Class": "B",
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
        for child in graph[node]["Children"]:
            G.add_edge(node, child, Category=graph[node]["Category"])
        G.nodes[node]["Children"] = graph[node]["Children"]
        G.nodes[node]["Parent"] = graph[node]["Parent"]
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, with_labels=True, pos=pos)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=nx.get_edge_attributes(G, "Category"))
    node_labels = {}
    for node in G.nodes:
        node_labels[node] = f"Children: {G.nodes[node]['Children']}\nParent: {G.nodes[node]['Parent']}"
    nx.draw_networkx_labels(G, pos=pos, labels=node_labels)
    plt.show()


def find_self_referencing_nodes(graph):
    """функция для нахождения узлов, которые ссылаются на себя"""
    error_nodes = []
    for node in graph:
        if graph[node]["Parent"] == node:
            error_nodes.append(node)
    return error_nodes


def find_B_to_F_nodes(graph):
    """функция для нахождения узлов класса B, ссылающихся на узлы класса F"""
    error_nodes = []
    for node in graph:
        if graph[node]["Category"] == "B":
            parent = graph[node]["Parent"]
            if parent is not None and graph[parent]["Category"] == "F":
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

    print("Самоссылка:")
    print(find_self_referencing_nodes(graph))

    print("Ошибка наследования:")
    print(find_B_to_F_nodes(graph))

    draw_graph(graph)
