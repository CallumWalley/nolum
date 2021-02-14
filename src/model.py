from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean, JSON, Date

Base = declarative_base()
# ANZ details example
# Type,             Details,                        Particulars,    Code,               Reference,  Amount, Date,       ForeignCurrencyAmount,      ConversionCharge
# Visa Purchase,    4835-****-****-2031  Df,        0.64,           Google  Clou,       0.21,       -12.07, 04/12/2019, USD 7.61 converted at 0.64, This includes a currency conversion charge of $0.21

class Transaction(Base):
    __tablename__:"transaction"

    id = Column(Integer, primary_key=True)
    raw_string = Column(String) # Raw unedited string.
    input_source = Column(String) # Where come from
    to_account = Column(String)
    from_account = Column(String)
    amount = Column(Numeric)
    pay_type = Column(String)
    details = Column(String)
    date = Column(Date)
    tags = Column(String)
    ml_data = Column(JSON)

class InputSource(Base):
    """A list of input sources (to avoid repeat injests)"""
    __tablename__:"input_source"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    filename = Column(String)
    ingest_date = Column(Datetime)
    sha1_sum = Column(Integer)

class Account(Base):
    """List of Transactions"""
    __tablename__:"account"
    id = Column(Integer, primary_key=True)
    entity = Column(String)

class Entitiy(Base):
    """Party owns Account"""
    __tablename__:"party"
    id = Column(Integer, primary_key=True)
    is_you = Column(Boolean), # If true, then sheets can be injested to this persons account. 

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




