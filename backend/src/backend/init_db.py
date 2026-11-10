from .database import engine, Base
from . import models

print("正在创建数据库表...")
Base.metadata.create_all(bind=engine)
print("建表完成！")