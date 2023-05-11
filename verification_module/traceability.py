"""В данном файле хранится класс тест-кейса с его конструктором и функция для связывания каждого требования с тест-кейсами"""

from verification_module.tree_builder import Graph


class TestCase:
    def __init__(self, req_id: int, test_steps: dict, expected_results: list):
        self.req_id = req_id
        self.test_steps = test_steps
        self.expected_results = expected_results

    def __repr__(self):
        return f"TestCase(req_id={self.req_id}, test_steps={self.test_steps}, expected_results={self.expected_results})"


def append_test_cases(reqs_graph: Graph, test_cases: list):
    """функция для связывания тест кейсов с требованиями"""
    for case in test_cases:
        req_node = reqs_graph.nodes[case.req_id]
        req_node.add_test(case)

