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
    labels = {}
    colors = {}
    for node in graph:
        category = graph[node]['Category']
        labels[node] = node
        if category not in colors:
            colors[category] = (random.random(), random.random(), random.random())
        G.add_node(node)
    for node in graph:
      for child in graph[node]['Children']:
          G.add_edge(node, child)
    node_colors = [colors[graph[node]['Category']] for node in graph]
    pos = nx.spring_layout(G, seed=42) # добавить атрибут seed
    sorted_pos = dict(sorted(pos.items())) # отсортировать словарь pos по ключам
    nx.draw(G, pos=sorted_pos, with_labels=True, labels=labels, node_color=node_colors, cmap='jet') # использовать sorted_pos и sorted_node_colors
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

def find_alone_Nodes(graph):
  """функция для нахождения одиночных узлов"""
  error_nodes = []
  for node in graph:
    if len(graph[node]['Children']) == 0 and graph[node]['Parent'] == None:
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

    print("Одиночные требования:")
    print(find_alone_Nodes(graph))

    draw_graph(graph)