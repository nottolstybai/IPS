# импортируем модуль json для работы с данными
import json

# загружаем данные из строки в переменную data
data = json.loads("""
[
  {
    "ID": 1,
    "Text": "Требование 1",
    "Comment": "Комментарий 1",
    "Class": "B",
    "Parent": 2
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
    # перебираем все требования в данных
    for req in data:
        # получаем ID, category и Parent текущего требования
        id = req["ID"]
        category = req["Class"]
        parent = req["Parent"]
        # если ID еще нет в словаре graph, то создаем пустой список для хранения дочерних узлов
        if id not in graph:
            graph[id] = {"Children": [], "Category": category, "Parent": parent}
        # если Parent не равен null, то добавляем ID в список дочерних узлов Parent
        if parent != None:
            # если Parent еще нет в словаре graph, то создаем пустой список для хранения дочерних узлов
            if parent not in graph:
                graph[parent] = {"Children": [], "Category": None, "Parent": None}
            # добавляем ID в список дочерних узлов Parent
            graph[parent]["Children"].append(id)
    # возвращаем граф
    return graph


def dfs(start, visited, path, graph, cycles):
    # добавляем текущий узел в список посещенных и путь
    visited.add(start)
    path.append(start)
    # находим все дочерние узлы текущего узла, если они есть в графе
    if start in graph:
        for child in graph[start]["Children"]:
            # если дочерний узел уже посещен, то это цикл
            if child in visited:
                # добавляем цикл в список циклов, если еще не добавили
                cycle = path[path.index(child):]
                # если цикл состоит из двух элементов, то сортируем его по возрастанию ID
                if len(cycle) == 2:
                    cycle.sort()
                if cycle not in cycles:
                    cycles.append(cycle)
            # иначе продолжаем поиск в глубину от дочернего узла
            else:
                dfs(child, visited, path, graph, cycles)
    # удаляем текущий узел из пути
    path.pop()


def find_self_referencing_nodes(graph):
    """функция для нахождения узлов, которые ссылаются на себя"""
    error_nodes = []
    for node in graph:
        if graph[node]["Parent"] == node:
            error_nodes.append(node)
    return error_nodes


# функция для нахождения узлов класса B, ссылающихся на узлы класса F
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

    cycles = []
    for node in graph:
        visited = set()
        path = []
        dfs(node, visited, path, graph, cycles)

    print("Найдены следующие циклы:")
    for cycle in cycles:
        print(cycle)

    print("Самоссылка:")
    print(find_self_referencing_nodes(graph))

    print("Ошибка наследования:")
    print(find_B_to_F_nodes(graph))
