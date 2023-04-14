from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dataBase import get_db
from schemas.branch import *
from utils.auth import Hasher, create_access_token
from models import Admin, password_reset
from utils.send_email import sendRegistrationMail, otp_generator

router = APIRouter(tags=["Admin Auth"])

@router.post('/adminResister')
def adminRegister(
    request: detail_register,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db), 
    ):

    row = db.query(Admin).filter(Admin.email == request.email)
    if row.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        detail = f"User with {request.email} is already exist")

    row = db.query(Admin).filter(Admin.mobile == request.mobile)
    if row.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
        detail = f"User with {request.mobile} is already exist")

    sendRegistrationMail(request.email, request.mobile, background_tasks)
    data = {
        "userName": request.userName,
        "password": Hasher.get_password_hash(request.password),
        "email": request.email,
        "mobile": request.mobile
    }

    user = Admin(**data)
    db.add(user)
    db.flush()
    data.update({"id": user.id})
    db.commit()
    access_token = create_access_token(data, EXPIRY=60)
    return {"data": request, "access_token": access_token, "token_type": "bearer"}

@router.post('/adminLogin')
def adminLogin(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    
    if request.username.isdigit():
        user = db.query(Admin
                ).filter(Admin.mobile == request.username).first()
    else:
        user = db.query(Admin
        ).filter(Admin.email == request.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    
    if not Hasher.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect Password")

    data = {
        "userName": user.userName,
        "password": Hasher.get_password_hash(user.password),
        "email": user.email,
        "mobile": user.mobile
    }

    access_token = create_access_token(data, EXPIRY=60)

    return {'message': "Login sucessfully", "access_token": access_token, "token_type": "bearer"}

@router.post("/adminForget", status_code=status.HTTP_200_OK)
def adminForgetPassword(inp: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if "@" in inp:
        user = db.query(Admin).filter(Admin.email == inp).first()
    else:
        user = db.query(Admin).filter(Admin.mobile == int(inp)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User does not exist"
                            )

    # Send OTP on email as well as mobile
    otp = otp_generator()
    mess = "Password reset"
    sendOTPemail(otp, user.email, mess, background_tasks)

    row = db.query(password_reset)\
        .filter(password_reset.user_email_id == inp)

    if not row.first():
        userData = password_reset(
            user_email_id=user.email,
            otp=otp
        )
        db.add(userData)
    else:
        row.update({
            password_reset.user_email_id: user.email,
            password_reset.otp: otp
        })

    db.commit()

    return{"message": "OTP has been sent to change password"}

@router.put("/adminChangePass", status_code=status.HTTP_200_OK)
def adminChangePassword(request: pass_reset, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(password_reset).filter(
        password_reset.user_email_id == request.email)

    if user.first().otp != request.otp:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Incorrect OTP"
                            )

    mess = "Your New Password is"
    sendConfirmInfo(request.password, request.email, mess, background_tasks)

    users = db.query(Admin).filter(
        Admin.email == request.email)

    users.update({"password": Hasher.get_password_hash(request.password)})
    db.commit()

    return {"message": "Password updated succesfully"}
