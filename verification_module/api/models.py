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


class InitialTestCase(BaseModel):
    ID_req: int
    Test: dict[str, str]
    expected_results: list[str]


class ReqsAndTests(BaseModel):
    reqs: list[InitialRequirement]
    tests: list[InitialTestCase]
