from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .database import get_db
from . import models, schemas, crud

app = FastAPI(title="MilkTeaMeter API - Phase 2")


# 1. 品牌列表（用 Schema 规范输出）
@app.get("/brands", response_model=List[schemas.BrandBase])
def read_brands(db: Session = Depends(get_db)):
    return crud.get_brands(db)


# 2. 某品牌下的饮品（注意这里我们用了 schema 里的 BrandWithDrinks）
@app.get("/brands/{brand_id}/drinks", response_model=schemas.BrandWithDrinks)
def read_drinks_by_brand(brand_id: int, db: Session = Depends(get_db)):
    brand = crud.get_drinks_by_brand(db, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    return brand


# 3. 饮品详情
@app.get("/drinks/{drink_id}", response_model=schemas.DrinkBase)
def read_drink(drink_id: int, db: Session = Depends(get_db)):
    drink = crud.get_drink(db, drink_id)
    if not drink:
        raise HTTPException(status_code=404, detail="饮品不存在")
    return drink


# 4. 热量估算（查数据库 + 规则计算）
@app.get("/drinks/{drink_id}/estimate")
def estimate_calories(
        drink_id: int,
        sweetness: str = Query("五分糖"),
        toppings: Optional[List[str]] = Query(None),
        db: Session = Depends(get_db)
):
    # 先查数据库拿基础数据
    drink = crud.get_drink(db, drink_id)
    if not drink:
        raise HTTPException(status_code=404, detail="饮品不存在")

    total = drink.base_calories

    # 甜度规则
    sweet_rules = {"全糖": 100, "七分糖": 70, "五分糖": 50, "三分糖": 30, "无糖": 0}
    if sweetness not in sweet_rules:
        raise HTTPException(status_code=400, detail="无效的甜度")
    total += sweet_rules[sweetness]

    # 小料规则
    topping_rules = {"珍珠": 66, "椰果": 30, "奶盖": 80, "芋圆": 50}
    if toppings:
        for t in toppings:
            if t in topping_rules:
                total += topping_rules[t]
            else:
                raise HTTPException(status_code=400, detail=f"无效的小料：{t}")

    return {
        "drink_name": drink.name,
        "base_calories": drink.base_calories,
        "sweetness": sweetness,
        "toppings": toppings or [],
        "estimated_total_calories": total
    }