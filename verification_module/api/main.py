"""Данный файл отвечает за оборачивание всего написанного функционала по 1 и 2 модулям в API,
   к которому будут отправляться запросы,
   для комплексной проверки требований (1 модуль)
   для комплексной проверки покрытия требований тест-кейсами (2 модуль)"""
import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.responses import Response

from verification_module.api.models import InitialRequirement, ReqsAndTests
from verification_module.api.utils import graph_init, check_test_cases, create_report, run_test_case_validation

app = FastAPI()


@app.post("/api/v1/module1")
async def get_failed_reqs(reqs: list[InitialRequirement]):
    graph = graph_init(reqs)

    error1 = graph.find_alone_nodes()
    error2 = graph.find_cycles()
    error3 = graph.find_BNodes_to_notBnodes()

    failed_nodes = {
        "status": not (error1 + error2 + error3),
        "alone_req_ids": error1,
        "cycled_req_ids": error2,
        "wrong_hierarchy_req_ids": error3}

    return failed_nodes


@app.post("/api/v1/module2")
async def get_not_covered_tests(reqs_and_tests: ReqsAndTests):
    graph = graph_init(reqs_and_tests.reqs)
    test_case_data = [test.__dict__ for test in reqs_and_tests.tests]
    check_test_cases(graph, test_case_data)
    error1 = graph.check_test_cases()
    return {
        "status": not error1,
        "not_covered_tests": error1}


@app.post("/api/v1/upload/reqs_tests_crosstab")
async def get_reqs_tests_excel(reqs_and_tests: ReqsAndTests):
    graph = graph_init(reqs_and_tests.reqs)
    test_case_data = [test.__dict__ for test in reqs_and_tests.tests]

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'export', 'output', 'reqs_tests.xlsx')

    df = check_test_cases(graph, test_case_data)
    df.to_excel(path)
    return FileResponse(path,
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.post("/api/v1/upload/report_module1")
async def upload_report_module1(reqs: list[InitialRequirement]):
    graph = graph_init(reqs)
    failed_nodes = {"alone_req_ids": graph.find_alone_nodes(),
                    "cycled_req_ids": graph.find_cycles(),
                    "wrong_hierarchy_req_ids": graph.find_BNodes_to_notBnodes()}

    contents = create_report(graph, failed_nodes, '../export/output/report_module1')
    response = Response(content=contents, media_type="application/pdf")
    response.headers["Content-Disposition"] = "attachment; filename=output.pdf"
    return response


@app.post("/api/v1/upload/report_module2")
async def upload_report_module2(reqs_and_tests: ReqsAndTests):
    graph = run_test_case_validation(reqs_and_tests)
    failed_nodes = {"not_covered_tests": graph.check_test_cases()}

    contents = create_report(graph, failed_nodes, '../export/output/report_module2')
    response = Response(content=contents, media_type="application/pdf")
    response.headers["Content-Disposition"] = "attachment; filename=output.pdf"
    return response


@app.post("/api/v1/upload/full_report")
async def upload_full_report(reqs_and_tests: ReqsAndTests):
    graph = run_test_case_validation(reqs_and_tests)
    failed_nodes = {"alone_req_ids": graph.find_alone_nodes(),
                    "cycled_req_ids": graph.find_cycles(),
                    "wrong_hierarchy_req_ids": graph.find_BNodes_to_notBnodes(),
                    "not_covered_tests": graph.check_test_cases()}

    contents = create_report(graph, failed_nodes, '../export/output/full_report.pdf')
    response = Response(content=contents, media_type="application/pdf")
    response.headers["Content-Disposition"] = "attachment; filename=output.pdf"
    return response


if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8080)
