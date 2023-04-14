from pydantic import BaseModel

class Branch_Detail(BaseModel):
    branchName: str = None
    branchAddress1: str = None
    branchAddress2: str = None
    branchCity: str = None
    branchState: int = None
    branchCountry: int = None
    branchPincode: int = None
    

class detail_register(BaseModel):
    userName: str = None
    password : str = None
    email: str = None
    mobile: int = None

class pass_reset(BaseModel):
    user_email_id: str = None
    password: str = None
    otp : str = None
    othersPassReset: str = None

class detail_product(BaseModel):
    productName: str = None
    description: str = None
    inStock: bool = None
    productCode: str = None
    gender: str = None
    category: str = None
    price: int = None
    taxes: bool = None

class detail_user(BaseModel):
    userName: str = None
    email: str = None
    phoneNumber: int = None
    country: str = None
    state: str = None
    city: str = None
    address: str = None
    zipCode: int = None
    company: str = None
    role: str = None
    isVerified: bool = None