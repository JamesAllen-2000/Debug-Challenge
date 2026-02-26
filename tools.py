## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import BaseTool
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from pypdf import PdfReader

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class _ReadFinancialDocumentInput(BaseModel):
    path: str = Field(default="data/sample.pdf", description="Path to a PDF file on disk")


class FinancialDocumentTool(BaseTool):
    name: str = "read_financial_document"
    description: str = "Read a financial PDF document from disk and return extracted text."
    args_schema: type[BaseModel] = _ReadFinancialDocumentInput

    def _run(self, path: str = "data/sample.pdf") -> str:
        if not os.path.exists(path):
            return f"File not found: {path}"

        reader = PdfReader(path)
        pages_text: list[str] = []
        for page in reader.pages:
            text = page.extract_text() or ""
            # Normalize excessive whitespace a bit
            while "\n\n" in text:
                text = text.replace("\n\n", "\n")
            pages_text.append(text)

        return "\n".join(pages_text).strip()


financial_document_tool = FinancialDocumentTool()

## Creating Investment Analysis Tool
class InvestmentTool:
    async def analyze_investment_tool(financial_document_data):
        # Process and analyze the financial document data
        processed_data = financial_document_data
        
        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        # TODO: Implement investment analysis logic here
        return "Investment analysis functionality to be implemented"

## Creating Risk Assessment Tool
class RiskTool:
    async def create_risk_assessment_tool(financial_document_data):        
        # TODO: Implement risk assessment logic here
        return "Risk assessment functionality to be implemented"