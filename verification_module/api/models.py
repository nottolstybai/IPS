"""В данном файле хранятся основные модели данных, которые присылаются в нашу систему:
    Требования (InitialRequirement)
    Тест-кейс (InitialTestCase)
    И набор из требований и тест-кейсов, которые приходят при обращении к 1 и 2 модулям (ReqsAndTests)
"""

from pydantic import BaseModel


class InitialRequirement(BaseModel):
    ID: int | None
    Text: str | None
    Comment: str | None
    Category: str | None
    Parent: int | None

class InitialFileGit(BaseModel):
    branchID: int | None
    filePath: str | None
    versionId: int | None




def from_dict_ir(d):
    ir = InitialRequirement({})
    ir.__dict__.update(d)
    return ir

def from_dict_it(d):
    it = InitialTestCase({})
    it.__dict__.update(d)
    return it

class InitialTestCase(BaseModel):
    ID_req: int
    Test: dict[str, str]
    expected_results: list[str]


class ReqsAndTests(BaseModel):
    reqs: list[InitialRequirement]
    tests: list[InitialTestCase]


class ReqsAndTestsFile(BaseModel):
    reqs: list[InitialFileGit]
    tests: list[InitialFileGit]
