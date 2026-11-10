from sqlalchemy.orm import Session
from . import models

def get_brands(db: Session):
    return db.query(models.Brand).all()

def get_drinks_by_brand(db: Session, brand_id: int):
    return db.query(models.Brand).filter(models.Brand.id == brand_id).first()

def get_drink(db: Session, drink_id: int):
    return db.query(models.Drink).filter(models.Drink.id == drink_id).first()