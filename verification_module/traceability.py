"""В данном файле хранится класс тест-кейса с его конструктором и функция для связывания каждого требования с тест-кейсами"""

from verification_module.tree_builder import Graph


class TestCase:
    test_count = 0

    def __init__(self, req_id: int, test_steps: dict, expected_results: list):
        TestCase.test_count += 1
        self.test_id = f'TestCase{TestCase.test_count}'
        self.req_id = req_id
        self.test_steps = test_steps
        self.expected_results = expected_results

    def __repr__(self):
        return f"TestCase(req_id={self.req_id}, test_steps={self.test_steps}, expected_results={self.expected_results})"


def append_test_cases(reqs_graph: Graph, test_cases: list):
    """функция для связывания тест кейсов с требованиями"""
    for case in test_cases:
        append_test_case_iter(reqs_graph, case, case.req_id)


def append_test_case_iter(graph: Graph, test_case: TestCase, req_id: int):
    req_node = graph.nodes[req_id]
    req_node.add_test(test_case)
    if req_node.parent is not None:
        append_test_case_iter(graph, test_case, req_node.parent)
    return
