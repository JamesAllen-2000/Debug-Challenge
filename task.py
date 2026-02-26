from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import financial_document_tool

verification = Task(
    description="Analyze the document located at {file_path} using the financial_document_tool. Verify whether it is a legitimate financial report.",
    expected_output="A confirmation of whether the document is a financial report, with a brief summary of its nature.",
    agent=verifier,
    tools=[financial_document_tool],
    async_execution=False
)

analyze_financial_document = Task(
    description="Using the document at {file_path}, perform a detailed financial analysis addressing the user's query: {query}",
    expected_output="A detailed financial analysis highlighting revenue, earnings, growth, and key metrics extracted from the document.",
    agent=financial_analyst,
    tools=[financial_document_tool],
    async_execution=False,
)

investment_analysis = Task(
    description="Based on the financial analysis of the document at {file_path}, formulate investment recommendations. Address the user query: {query}",
    expected_output="Professional investment recommendations mapping the financial analysis to actionable advice.",
    agent=investment_advisor,
    tools=[financial_document_tool],
    async_execution=False,
)

risk_assessment = Task(
    description="Identify key risk factors from the document at {file_path} and assess their potential impact on investments.",
    expected_output="A comprehensive risk assessment detailing market, operational, and financial risks.",
    agent=risk_assessor,
    tools=[financial_document_tool],
    async_execution=False,
)