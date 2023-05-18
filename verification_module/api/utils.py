from verification_module.api.models import InitialRequirement
from verification_module.traceability import append_test_cases, TestCase
from verification_module.tree_builder import Graph


def graph_init(reqs: list[InitialRequirement]):
    data = [req.__dict__ for req in reqs]
    graph = Graph()
    graph.create_from_data(data)
    return graph


def check_test_cases(graph: Graph, test_case_data: list):
    test_cases = []
    for test_data in test_case_data:
        test_case = TestCase(req_id=test_data["ID_req"],
                             test_steps=test_data["Test"],
                             expected_results=test_data["expected_results"])
        test_cases.append(test_case)
    append_test_cases(graph, test_cases)
    return graph
