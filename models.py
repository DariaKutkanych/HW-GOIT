from datetime import datetime
from enum import unique
from locale import currency

from sqlalchemy import Column, Integer, String, Float, Date, UniqueConstraint
from sqlalchemy.sql.sqltypes import DateTime

from db import Base, engine


class Rate(Base):
    __tablename__ = "rates"
    __table_args__ = (UniqueConstraint('bank', 'created', 'currency', name="date_already_added"),)
    id = Column(Integer, primary_key=True)
    bank = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    rate = Column(Float, nullable=False)
    created = Column(Date, default=datetime.now().date)
    
    def __repr__(self) -> str:
        return f"{self.bank} {self.currency} {self.rate} {self.created}"

if __name__ == "__main__":
    Base.metadata.create_all(engine)