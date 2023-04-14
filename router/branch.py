from fastapi import APIRouter, Depends
from dataBase import get_db
from schemas.branch import Branch_Detail
from sqlalchemy.orm import Session
from models import Branch

router = APIRouter(tags=["Branch"])

@router.post("/branch")
def create_branch(
    request: Branch_Detail, 
    db: Session = Depends(get_db)):

    row = db.query(Branch
                ).filter(Branch.branchName == request.branchName
                    ).first()
    
    if row:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSIBE_ENTITY, 
            detail = "Branch by name {request.branchName} is already Exist")

    branch = Branch(
        branchName = request.branchName,
        branchAddress1 = request.branchAddress1,
        branchAddress2 = request.branchAddress2,
        branchPincode = request.branchPincode,
        branchCity = request.branchCity,
        branchState = request.branchState,
        branchCountry = request.branchCountry
    )

    db.add(branch)
    db.commit()

    return {"message": "Branch has been created sucessfully"}

@router.get("/branch/{ID}")
def getBranch(
    ID: int, 
    db: Session = Depends(get_db)):

    row = db.query(Branch).filter(Branch.id == ID).first()

    if not row:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No branch found")

    return row

@router.put("/branch/{ID}")
def updateBranch(
    ID: int, 
    request: Branch_Detail,
    db: Session = Depends(get_db)):

    row = db.query(Branch).filter(Branch.id == ID)

    if not row.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No branch found")

    if row.first().branchName == request.branchName and row.first().id != ID:
        raise HTTPException(status_code = status.HTTP_208_ALREADY_EXIST, detail = "Branch already exst with name {request.branchName}")

    row.update({
        Branch.branchName: request.branchName,
        Branch.branchAddress1: request.branchAddress1,
        Branch.branchAddress2: request.branchAddress2,
        Branch.branchCity: request.branchCity,
        Branch.branchState: request.branchState,
        Branch.branchCountry: request.branchCountry,
        Branch.branchPincode: request.branchPincode
    })

    db.commit()

    return {"message": "Branch update sucessfully"}

@router.get("/branch")
def getAllBranches(db: Session = Depends(get_db)):

    rows = db.query(Branch).all()

    if not rows:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No branch found")

    return rows

@router.delete("/branch/{ID}")
def deleteBranch(ID: int, db: Session = Depends(get_db)):

    row = db.query(Branch).filter(Branch.id == ID)

    if not row.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No branch found")

    row.delete()
    db.commit()

    return {"message": "Branch has been deleted sucessfully"}
