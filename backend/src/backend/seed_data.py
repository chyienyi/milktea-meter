from .database import SessionLocal
from . import models


def seed_database():
    db = SessionLocal()

    # 检查是否已有数据
    if db.query(models.Brand).first():
        print("数据库已有数据，跳过。")
        db.close()
        return

    # 1. 插入品牌
    brand1 = models.Brand(name="一点点")
    brand2 = models.Brand(name="霸王茶姬")
    db.add_all([brand1, brand2])
    db.commit()
    db.refresh(brand1)
    db.refresh(brand2)

    # 2. 插入饮品
    drinks = [
        models.Drink(name="波霸奶茶", base_calories=300, brand_id=brand1.id),
        models.Drink(name="四季奶青", base_calories=250, brand_id=brand1.id),
        models.Drink(name="伯牙绝弦", base_calories=280, brand_id=brand2.id),
        models.Drink(name="桂馥兰香", base_calories=260, brand_id=brand2.id)
    ]
    db.add_all(drinks)
    db.commit()
    db.close()
    print("初始数据写入成功！")


if __name__ == "__main__":
    seed_database()