from fastapi import APIRouter, Depends, HTTPException, status
from dataBase import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Review"])

@router.post('/review')
def createReview(db: Session = Depends(get_db)):
    pass

@router.get('/review')
def getAllReview(db: Session = Depends(get_db)):
    pass
 