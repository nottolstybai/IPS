import os

from verification_module.api.models import InitialRequirement, ReqsAndTests
from verification_module.export.reporter import ReporterPDF
from verification_module.traceability import append_test_cases, TestCase
from verification_module.tree_builder import Graph


def graph_init(reqs: list[InitialRequirement]) -> Graph:
    data = [req.__dict__ for req in reqs]
    graph = Graph()
    graph.create_from_data(data)
    return graph


def check_test_cases(graph: Graph, test_case_data: list) -> Graph:
    test_cases = []
    for test_data in test_case_data:
        test_case = TestCase(req_id=test_data["ID_req"],
                             test_steps=test_data["Test"],
                             expected_results=test_data["expected_results"])
        test_cases.append(test_case)
    append_test_cases(graph, test_cases)
    return graph


def run_test_case_validation(reqs_and_tests: ReqsAndTests):
    graph = graph_init(reqs_and_tests.reqs)
    test_case_data = [test.__dict__ for test in reqs_and_tests.tests]
    check_test_cases(graph, test_case_data)
    return graph


def create_report(graph: Graph, failed_nodes: dict, relative_fpath: str) -> bytes:
    reporter = ReporterPDF(graph, **failed_nodes)
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{relative_fpath}')
    reporter.create_artifact(report_path)
    with open(report_path, "rb") as file:
        contents = file.read()
    return contents
