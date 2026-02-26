import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, LLM

from tools import financial_document_tool

llm = LLM(model="gpt-4")

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide professional and accurate financial analysis based on the document provided to answer the user's query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned financial analyst with extensive experience in reading corporate financial reports."
        "You provide fact-based, objective financial analysis and insights."
    ),
    tools=[financial_document_tool],
    llm=llm,
    max_iter=3,
    allow_delegation=False
)

verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify the authenticity and relevance of the uploaded document.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a compliance officer responsible for ensuring that documents provided are indeed valid financial reports."
        "You carefully extract text and determine if it represents a corporate report or financial statement."
    ),
    tools=[financial_document_tool],
    llm=llm,
    max_iter=3,
    allow_delegation=False
)

investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide sound investment recommendations based on the financial analysis.",
    verbose=True,
    backstory=(
        "You are a fiduciary investment advisor known for evidence-based recommendations."
        "You focus on long-term value, assessing company fundamentals and market conditions."
    ),
    tools=[financial_document_tool],
    llm=llm,
    max_iter=3,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="Evaluate and highlight the potential risks associated with the company's financials.",
    verbose=True,
    backstory=(
        "You are a precise and analytical risk manager. You identify potential financial risks, market vulnerabilities, and operational threats from documents."
    ),
    tools=[financial_document_tool],
    llm=llm,
    max_iter=3,
    allow_delegation=False
)
