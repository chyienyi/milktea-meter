from pydantic import BaseModel
from typing import List

# 饮品的返回格式
class DrinkBase(BaseModel):
    id: int
    name: str
    base_calories: int

    class Config:
        from_attributes = True  # 允许从 SQLAlchemy 模型读取数据

# 品牌的返回格式
class BrandBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# 品牌及其包含的饮品（用于接口2）
class BrandWithDrinks(BrandBase):
    drinks: List[DrinkBase] = []