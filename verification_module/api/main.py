"""Данный файл отвечает за оборачивание всего написанного функционала по 1 и 2 модулям в API,
к которому будут отправляться запросы,
    для комплексной проверки требований (1 модуль)
    для комплексной проверки покрытия требований тест-кейсами (2 модуль)"""
import os

import uvicorn
from fastapi import FastAPI
from starlette.responses import Response

from verification_module.api.models import InitialRequirement, ReqsAndTests
from verification_module.api.utils import graph_init, check_test_cases
from verification_module.export.reporter import ReporterPDF

app = FastAPI()


@app.post("/api/v1/module1")
async def get_failed_reqs(reqs: list[InitialRequirement]):
    graph = graph_init(reqs)
    failed_nodes = {"alone_req_ids": graph.find_alone_nodes(),
                    "cycled_req_ids": graph.find_cycles(),
                    "wrong_hierarchy_req_ids": graph.find_BNodes_to_notBnodes()}

    return failed_nodes


@app.post("/api/v1/module2")
async def get_not_covered_tests(reqs_and_tests: ReqsAndTests):
    graph = graph_init(reqs_and_tests.reqs)
    test_case_data = [test.__dict__ for test in reqs_and_tests.tests]
    check_test_cases(graph, test_case_data)
    return {"not_covered_tests": graph.check_test_cases()}


@app.post("/api/v1/upload/full_report")
async def upload_full_report(reqs_and_tests: ReqsAndTests):
    graph = graph_init(reqs_and_tests.reqs)
    test_case_data = [test.__dict__ for test in reqs_and_tests.tests]
    check_test_cases(graph, test_case_data)

    failed_nodes = {"alone_req_ids": graph.find_alone_nodes(),
                    "cycled_req_ids": graph.find_cycles(),
                    "wrong_hierarchy_req_ids": graph.find_BNodes_to_notBnodes(),
                    "not_covered_tests": graph.check_test_cases()}
    print(graph)

    reporter = ReporterPDF(graph, **failed_nodes)
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'export', 'output', 'full_report.pdf')
    reporter.create_artifact(report_path)

    with open(report_path, "rb") as file:
        contents = file.read()
    response = Response(content=contents, media_type="application/pdf")
    response.headers["Content-Disposition"] = "attachment; filename=output.pdf"
    return response

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8080)
