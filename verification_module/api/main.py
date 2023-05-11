"""Данный файл отвечает за оборачивание всего написанного функционала по 1 и 2 модулям в API,
к которому будут отправляться запросы,
    для комплексной проверки требований (1 модуль)
    для комплексной проверки покрытия требований тест-кейсами (2 модуль)"""

import uvicorn
from fastapi import FastAPI

from verification_module.api.models import InitialRequirement, ReqsAndTests
from verification_module.traceability import TestCase, append_test_cases
from verification_module.tree_builder import Graph

app = FastAPI()


def graph_init(reqs: list[InitialRequirement]):
    data = [req.__dict__ for req in reqs]
    graph = Graph()
    graph.create_from_data(data)
    return graph


@app.post("/api/v1/module1")
async def check_reqs(reqs: list[InitialRequirement]):
    graph = graph_init(reqs)
    failed_nodes = {"alone_req_ids": graph.find_alone_nodes(),
                    "cycled_req_ids": graph.find_cycles(),
                    "wrong_hierarchy_req_ids": graph.find_BNodes_to_notBnodes()}

    return failed_nodes


@app.post("/api/v1/module2")
async def check_test_cases(reqs_and_tests: ReqsAndTests):
    graph = graph_init(reqs_and_tests.reqs)
    test_case_data = [test.__dict__ for test in reqs_and_tests.tests]
    test_cases = []
    for test_data in test_case_data:
        test_case = TestCase(req_id=test_data["ID_req"],
                             test_steps=test_data["Test"],
                             expected_results=test_data["expected_result"])
        test_cases.append(test_case)

    append_test_cases(graph, test_cases)
    return {"not_covered_tests": graph.check_test_cases()}


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8080)
