import json

from verification_module.tree_builder import Graph


class TestCase:
    def __init__(self, req_id: int, test_steps: dict, expected_results: list):
        self.req_id = req_id
        self.test_steps = test_steps
        self.expected_results = expected_results


def append_test_cases(reqs_graph: Graph, test_cases: list[TestCase]):
    """функция для связывания тест кейсов с требованиями"""
    for case in test_cases:
        req_node = reqs_graph.nodes[case.req_id]
        req_node.add_test(case)
