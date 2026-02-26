from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./financial_analysis.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class AnalysisTaskDB(Base):
    __tablename__ = "analysis_tasks"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, default="PROCESSING")
    file_name = Column(String)
    query = Column(String)
    analysis_result = Column(Text, nullable=True)

Base.metadata.create_all(bind=engine)
