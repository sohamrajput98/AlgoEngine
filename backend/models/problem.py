from sqlalchemy import Column, Integer, String, Boolean, Text
from .base import Base

class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    concept = Column(String(50), nullable=False)   # e.g., "sliding window"
    stars = Column(Integer, nullable=False)        # 1 to 5
    series_id = Column(Integer, nullable=True)     # group ID for related problems
    series_index = Column(Integer, nullable=True)  # order inside series
    is_daily_candidate = Column(Boolean, default=True)
