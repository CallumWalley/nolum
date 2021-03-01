from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean, JSON, Date, create_engine

from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
# ANZ details example
# Type,             Details,                        Particulars,    Code,               Reference,  Amount, Date,       ForeignCurrencyAmount,      ConversionCharge
# Visa Purchase,    4835-****-****-2031  Df,        0.64,           Google  Clou,       0.21,       -12.07, 04/12/2019, USD 7.61 converted at 0.64, This includes a currency conversion charge of $0.21

class BankTransaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)
    raw_string = Column(String) # Raw unedited string.
    # input_source = Column(String) # Where come from
    input_source_id = Column(Integer,ForeignKey("input_source.id"))
    to_account_id = Column(Integer, ForeignKey("account.id"))
    from_account_id = Column(Integer, ForeignKey("account.id"))
    amount = Column(Numeric)
    pay_type = Column(String)
    details = Column(String)
    date = Column(Date)
    tags = Column(String)
    ml_data = Column(JSON)

    # Relationships
    input_source = relationship("InputSource")
    to_account = relationship("Account", foreign_keys=[to_account_id])
    from_account = relationship("Account", foreign_keys=[from_account_id])

class InputSource(Base):
    """A list of input sources (to avoid repeat injests)"""
    __tablename__ = "input_source"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    filename = Column(String)
    ingest_date = Column(Date)
    hd5sum = Column(Integer) 

class Account(Base):
    """List of Transactions"""
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey("party.id"))
    entity = relationship("Entity")

class Entity(Base):
    """Party owns Account"""
    __tablename__ = "party"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_you = Column(Boolean) # If true, then sheets can be injested to this persons account. 

# class Invoiceable(Base):

# class WorkHour(Invoiceable):

# class Misc(Invoiceable):




# class Invoice(Base):
#     """Two entities and a list of hours"""
#     __tablename__:"invoice"
#     id = Column(Integer, primary_key=True)
#     is_paid = Column(Bool)
#     entity_paying = 
#     entity_receiving =

def create_session_maker():
    engine = create_engine("sqlite:///data.db")
    Base.metadata.create_all(engine)
    return sessionmaker(engine)