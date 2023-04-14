from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas.branch import *
from dataBase import get_db
from models import Product

router = APIRouter(tags=["Product"])

@router.post("/product")
def create_product(
    request: detail_product, 
    db: Session = Depends(get_db)):

    row = db.query(Product
                ).filter(Product.productName == request.productName
                    ).first()
    
    if row:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSIBE_ENTITY, 
            detail = "Product by name {request.productName} is already Exist")

    product = Product(
        productName = request.productName,
        description = request.description,
        inStock = request.inStock,
        productCode = request.productCode,
        gender = request.gender,
        category = request.category,
        price = request.price,
        taxes = request.taxes
    )

    db.add(product)
    db.commit()

    return {"message": "Product has been saved"}

@router.get("/product/{ID}")
def getProduct(
    ID: int, 
    db: Session = Depends(get_db)):

    row = db.query(Product).filter(Product.id == ID).first()

    if not row:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No product found")

    return row

@router.put("/product/{ID}")
def updateProduct(
    ID: int, 
    request: detail_product,
    db: Session = Depends(get_db)):

    row = db.query(Product).filter(Product.id == ID)

    if not row.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No product found")

    if row.first().productName == request.productName and row.first().id != ID:
        raise HTTPException(status_code = status.HTTP_208_ALREADY_EXIST, detail = "Product already exst with name {request.productName}")

    row.update({
        Product.productName: request.productName,
        Product.description: request.description,
        Product.inStock: request.inStock,
        Product.productCode: request.productCode,
        Product.gender: request.gender,
        Product.category: request.category,
        Product.price: request.price,
        Product.taxes: request.taxes
    })

    db.commit()

    return {"message": "Porduct update sucessfully"}

@router.get("/products")
def getAllProducts(db: Session = Depends(get_db)):

    rows = db.query(Product).all()

    if not rows:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No product found")

    return rows

@router.delete("/product/{ID}")
def deleteProduct(ID: int, db: Session = Depends(get_db)):

    row = db.query(Product).filter(Product.id == ID)

    if not row.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No product found")

    row.delete()
    db.commit()

    return {"message": "Product has been deleted sucessfully"}
