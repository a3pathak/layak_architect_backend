from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.branch import *
from models import User, password_reset
from dataBase import get_db
from utils.send_email import sendRegistrationMail, otp_generator

router = APIRouter(tags=["User"])

@router.post("/user")
def create_user(
    request: detail_user, 
    db: Session = Depends(get_db)):

    print(request)

    row = db.query(User
                ).filter(User.userName == request.userName
                    ).first()
    
    if row:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSIBE_ENTITY, 
            detail = "User by name {request.userName} is already Exist")

    user = User(
        userName = request.userName,
        email = request.email,
        phoneNumber = request.phoneNumber,
        country = request.country,
        state = request.state,
        city = request.city,
        address = request.address,
        zipCode = request.zipCode,
        company = request.company,
        role = request.role,
        isVerified = request.isVerified
    )

    db.add(user)
    db.commit()

    return {"message": "User has been saved"}

@router.get("/user/{ID}")
def getProduct(
    ID: int, 
    db: Session = Depends(get_db)):

    row = db.query(User).filter(User.id == ID).first()

    if not row:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No user found")

    return row

@router.put("/user/{ID}")
def updateUser( 
    ID: int, 
    request: detail_user,
    db: Session = Depends(get_db)):

    row = db.query(User).filter(User.id == ID)

    if not row.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No user found")

    if row.first().userName == request.userName and row.first().id != ID:
        raise HTTPException(status_code = status.HTTP_208_ALREADY_EXIST, detail = "User already exst with name {request.userName}")

    row.update({
        User.userName: request.userName,
        User.email: request.email,
        User.phoneNumber: request.phoneNumber,
        User.country: request.country,
        User.state: request.state,
        User.city: request.city,
        User.address: request.address,
        User.zipCode: request.zipCode,
        User.company: request.company,
        User.role: request.role,
        User.isVerified: request.isVerified
    })

    db.commit()

    return {"message": "User update sucessfully"}

@router.get("/users")
def getAllUser(db: Session = Depends(get_db)):

    rows = db.query(User).all()

    if not rows:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No user found")

    return rows

@router.delete("/user/{ID}")
def deleteUser(
    ID: int, 
    db: Session = Depends(get_db)):

    row = db.query(User).filter(User.id == ID)

    if not row.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No user found")

    row.delete()
    db.commit()

    return {"message": "User has been deleted sucessfully"}



