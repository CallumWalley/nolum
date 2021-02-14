from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean

Base = declarative_base()

class Transaction(Base):
    __tablename__:"transaction"

    id = Column(Integer, primary_key=True)
    to_entity = Column(String)
    from_entity = Column(String)
    amount = Column(Numeric)
    is_credit = Column(Boolean)