import os
from docxtpl import DocxTemplate
from resume_writer.models.resume import ResumeData

class ResumeRenderer:
    def __init__(self, template_path: str):
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found at {template_path}")
        self.template_path = template_path

    def render(self, data: ResumeData, output_path: str) -> str:
        """
        Renders the ResumeData into the docxtpl document.
        """
        doc = DocxTemplate(self.template_path)
        context = data.model_dump()
        doc.render(context)
        doc.save(output_path)
        return output_path
