from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class TestCase(Base):
    __tablename__ = "testcases"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    input_data = Column(String(1000), nullable=False)
    expected_output = Column(String(1000), nullable=False)
    is_sample = Column(Boolean, default=False)

    problem = relationship("Problem", backref="testcases")
