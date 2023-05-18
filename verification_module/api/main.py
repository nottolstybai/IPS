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

    error1 = graph.find_alone_nodes()
    error2 = graph.find_cycles()
    error3 = graph.find_BNodes_to_notBnodes()

    status = (len(error1) + len(error2) + len(error3)) == 0

    failed_nodes = {
        "status": status
        "alone_req_ids": error1,
        "cycled_req_ids": error2,
        "wrong_hierarchy_req_ids": error3}

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
    error1 = graph.check_test_cases()
    status = len(error1) == 0;
    return {
        "status": status
        "not_covered_tests": graph.check_test_cases()}


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8080)
