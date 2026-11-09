from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
import json
import os

app = FastAPI(title="MilkTeaMeter API - Phase 1")

# ================= 1. 准备内存数据 =================
# 为了让你立刻能跑，我们先写死在内存里（模拟数据库）
# 包含 3 个品牌，每个品牌多款饮品，附带 ID
BRANDS_DB = [
    {"id": 1, "name": "一点点"},
    {"id": 2, "name": "喜茶"},
    {"id": 3, "name": "霸王茶姬"}
]

DRINKS_DB = [
    # 一点点 (brand_id: 1)
    {"id": 101, "brand_id": 1, "name": "波霸奶茶", "base_calories": 300},
    {"id": 102, "brand_id": 1, "name": "四季奶青", "base_calories": 250},
    {"id": 103, "brand_id": 1, "name": "红茶玛奇朵", "base_calories": 280},

    # 喜茶 (brand_id: 2)
    {"id": 201, "brand_id": 2, "name": "多肉葡萄", "base_calories": 320},
    {"id": 202, "brand_id": 2, "name": "芝芝莓莓", "base_calories": 350},

    # 霸王茶姬 (brand_id: 3)
    {"id": 301, "brand_id": 3, "name": "伯牙绝弦", "base_calories": 280},
    {"id": 302, "brand_id": 3, "name": "桂馥兰香", "base_calories": 260}
]

# 热量增量规则字典
SWEETNESS_RULES = {"全糖": 100, "七分糖": 70, "五分糖": 50, "三分糖": 30, "无糖": 0}
TOPPING_RULES = {"珍珠": 66, "椰果": 30, "奶盖": 80, "芋圆": 50}


# ================= 2. 编写 4 个接口 =================

# 接口 1：品牌列表
@app.get("/brands")
def get_brands():
    return {"data": BRANDS_DB}


# 接口 2：某品牌下的饮品列表
@app.get("/brands/{brand_id}/drinks")
def get_drinks_by_brand(brand_id: int):
    # 先检查品牌是否存在
    brand = next((b for b in BRANDS_DB if b["id"] == brand_id), None)
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")

    # 筛选出属于该品牌的饮品
    drinks = [d for d in DRINKS_DB if d["brand_id"] == brand_id]
    return {"brand": brand["name"], "data": drinks}


# 接口 3：饮品详情
@app.get("/drinks/{drink_id}")
def get_drink_detail(drink_id: int):
    drink = next((d for d in DRINKS_DB if d["id"] == drink_id), None)
    if not drink:
        raise HTTPException(status_code=404, detail="饮品不存在")
    return {"data": drink}


# 接口 4：热量估算（核心亮点接口）
@app.get("/drinks/{drink_id}/estimate")
def estimate_calories(
        drink_id: int,
        sweetness: str = Query("五分糖", description="甜度选项"),
        toppings: Optional[List[str]] = Query(None, description="小料列表，可多选")
):
    # 1. 查基础饮品
    drink = next((d for d in DRINKS_DB if d["id"] == drink_id), None)
    if not drink:
        raise HTTPException(status_code=404, detail="饮品不存在")

    # 2. 算基础热量
    total = drink["base_calories"]

    # 3. 加上甜度热量
    if sweetness not in SWEETNESS_RULES:
        raise HTTPException(status_code=400, detail=f"无效的甜度选项，支持：{list(SWEETNESS_RULES.keys())}")
    total += SWEETNESS_RULES[sweetness]

    # 4. 加上小料热量
    if toppings:
        for t in toppings:
            if t in TOPPING_RULES:
                total += TOPPING_RULES[t]
            else:
                raise HTTPException(status_code=400, detail=f"无效的小料：{t}")

    return {
        "drink_name": drink["name"],
        "base_calories": drink["base_calories"],
        "sweetness": sweetness,
        "toppings": toppings if toppings else [],
        "estimated_total_calories": total
    }