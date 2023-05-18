
import json
from verification_module.traceability import TestCase, append_test_cases
from verification_module.tree_builder import Graph

data = json.loads("""
[
  {
    "ID": 1,
    "Text": "Требование 1",
    "Comment": "Комментарий 1",
    "Category": "B",
    "Parent": null
  },
  {
    "ID": 2,
    "Text": "Требование 2",
    "Comment": "Комментарий 2",
    "Category": "B",
    "Parent": 1
  },
  {
    "ID": 3,
    "Text": "Требование 3",
    "Comment": null,
    "Category": "F",
    "Parent": 1
  },
  {
    "ID": 4,
    "Text": "Требование 4",
    "Comment": null,
    "Category": "F",
    "Parent": 2
  },
  {
    "ID": 5,
    "Text": "Требование 5",
    "Comment": null,
    "Category": "F",
    "Parent": 2
  }
]
""")
test_case_data = [
{
  "ID_req": 3,
  "Test": {
    "1": "1 шаг",
    "2": "2 шаг",
    "3": "3 шаг",
    "4": "4 шаг"
  },
  "expected_result": [
    "Результат 1",
    "Результат 2",
    "Результат 3"
  ]
},
{
  "ID_req": 4,
  "Test": {
    "1": "1 шаг",
    "2": "2 шаг",
    "3": "3 шаг",
    "4": "4 шаг"
  },
  "expected_result": [
    "Результат 1",
    "Результат 2",
    "Результат 3"
  ]
},
{
  "ID_req": 5,
  "Test": {
    "1": "1 шаг",
    "2": "2 шаг",
    "3": "3 шаг",
    "4": "4 шаг"
  },
  "expected_result": [
    "Результат 1",
    "Результат 2",
    "Результат 3"
  ]
}

]


if __name__ == '__main__':
    graph1 = Graph()
    graph1.create_from_data(data)
    print(graph1)

    print(graph1.find_alone_nodes())
    print(graph1.find_cycles())
    print(graph1.find_BNodes_to_notBnodes())
    graph1.draw_graph()

    test_cases = []
    for test_data in test_case_data:
        test_case = TestCase(req_id=test_data["ID_req"],
                             test_steps=test_data["Test"],
                             expected_results=test_data["expected_result"])
        test_cases.append(test_case)

    append_test_cases(graph1, test_cases)


    print(graph1.check_test_cases())



