import os
from pypdf import PdfReader
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class _ReadFinancialDocumentInput(BaseModel):
    path: str = Field(default="data/sample.pdf", description="Path to a PDF file on disk")

class FinancialDocumentTool(BaseTool):
    name: str = "read_financial_document"
    description: str = "Read a financial PDF document from disk and return extracted text."
    args_schema: type[BaseModel] = _ReadFinancialDocumentInput

    def _run(self, path: str = "data/sample.pdf", **kwargs) -> str:
        if not os.path.exists(path):
            return f"File not found: {path}"

        try:
            reader = PdfReader(path)
            pages_text: list[str] = []
            for page in reader.pages:
                text = page.extract_text() or ""
                while "\n\n" in text:
                    text = text.replace("\n\n", "\n")
                pages_text.append(text)

            return "\n".join(pages_text).strip()
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"

financial_document_tool = FinancialDocumentTool()