from pydantic import BaseModel


class InitialRequirement(BaseModel):
    ID: int
    Text: str
    Comment: str
    Category: str
    Parent: str


class InitialTestCase(BaseModel):
    ID_req: int
    Test: dict[str, str]
    expected_result: list[str]


class ReqsAndTests(BaseModel):
    reqs: list[InitialRequirement]
    tests: list[InitialTestCase]
