from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from verification_module.tree_builder import Graph


class Reporter:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.x_axis = None
        self.y_axis = None
        self.canvas = None

    def create_artifact(self, artifact_name: str):
        pass


class ReporterPDF(Reporter):
    def __init__(
            self,
            graph: Graph,
            alone_req_ids: list,
            cycled_req_ids: list,
            wrong_hierarchy_req_ids: list,
            not_covered_tests: list
    ):
        super().__init__(graph)
        self.alone_req_ids = alone_req_ids
        self.cycled_req_ids = cycled_req_ids
        self.wrong_hierarchy_req_ids = wrong_hierarchy_req_ids
        self.no_tests_reqs = not_covered_tests

    def create_artifact(self, artifact_name: str):
        self.setup_canvas(artifact_name)
        self.add_title("REPORT")
        self.y_axis -= 20
        self.add_section("Verify requirements", [
            f"Ids of alone requirements without links: {', '.join(map(str, self.alone_req_ids))}",
            f"Ids of looped requirements: {', '.join(map(str, self.cycled_req_ids))}",
            f"Ids of requirements with a wrong hierarchy: {', '.join(map(str, self.wrong_hierarchy_req_ids))}"
        ])
        self.add_section("Check testcases", [
            f"Ids of uncovered by tests requirements: {', '.join(map(str, self.alone_req_ids))}"
        ])
        self.add_title("Requirements graph")
        self.add_image(self.graph.draw_graph())

        self.canvas.save()

    def setup_canvas(self, artifact_name: str):
        self.canvas = canvas.Canvas(artifact_name, pagesize=letter)
        self.canvas.setFont("Courier", 12)
        self.x_axis = 50
        self.y_axis = 750

    def add_title(self, title):
        new_styles = getSampleStyleSheet()
        heading_styles = new_styles['Heading1']
        p = Paragraph(title, heading_styles)
        p.wrapOn(self.canvas, 400, 400)
        p.drawOn(self.canvas, self.x_axis, self.y_axis)
        self.y_axis -= 20

    def add_section(self, section_title, content):
        self.add_title(section_title)
        for item in content:
            self.canvas.drawString(self.x_axis, self.y_axis, item)
            self.y_axis -= 20
        self.y_axis -= 20

    def add_image(self, image):
        self.y_axis -= 300
        self.canvas.drawImage(ImageReader(image), self.x_axis, self.y_axis - 60, width=400, height=300)
