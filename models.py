from email.policy import default
from sqlalchemy import Column, Integer, String, BigInteger, Boolean
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any

@as_declarative()
class Base:
    id: Any
    __name__: str

    #to generate tablename from classname
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class Admin(Base):
    id = Column(Integer, index= True, primary_key = True)
    userName = Column(String(500), default = None)
    password = Column(String(500), default = None)
    email = Column(String(500), unique=True, default = None)
    mobile = Column(BigInteger, unique=True, default = None)    

class password_reset(Base):
    id = Column(Integer, index= True, primary_key = True)
    user_email_id = Column(String(500), nullable=False, unique=True)
    otp = Column(Integer, default = None)
    othersPassReset = Column(String(500), default="")

class Product(Base):
    id = Column(Integer, index= True, primary_key = True)
    productName = Column(String(500), default = None)
    description = Column(String(10000), default = None)
    inStock = Column(Boolean, default = False)
    productCode = Column(String(500), default = None)    
    gender = Column(String(500), default = None)    
    category = Column(String(500), default = None)    
    price = Column(Integer, default = None)    
    taxes = Column(Boolean, default = False)   
    
class Branch(Base):
    id = Column(Integer, index= True, primary_key = True)
    branchName = Column(String(500), default = None)
    branchAddress1 = Column(String(500), default = None)
    branchAddress2 = Column(String(500), default = None)
    branchCity = Column(String(500), default = None)    
    branchState = Column(Integer, default = None)    
    branchCountry = Column(Integer, default = None)    
    branchPincode = Column(Integer, default = None)

class User(Base):
    id = Column(Integer, index= True, primary_key = True)
    userName = Column(String(500), default = None)
    email = Column(String(500), default = None)
    phoneNumber = Column(BigInteger, default = False)
    country = Column(String(500), default = None)    
    state = Column(String(500), default = None)    
    city = Column(String(500), default = None)    
    address = Column(String(500), default = None)    
    zipCode = Column(String(500), default = False)
    company = Column(String(500), default = False)   
    role = Column(String(500), default = False)   
    isVerified = Column(Boolean, default = False)   