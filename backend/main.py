import json
import os


# 1. 定义一个“饮品”类（Drink）
class Drink:
    def __init__(self, brand, name, base_calories):
        self.brand = brand
        self.name = name
        self.base_calories = base_calories

    # 定义打印这个对象时显示的内容
    def __str__(self):
        return f"{self.brand} - {self.name}"


# 2. 定义一个“热量计算器”类（CalorieEstimator）
class CalorieEstimator:
    def __init__(self, drink):
        # 组合模式：计算器里面“包含”了一个饮品对象
        self.drink = drink

    def calculate(self, sweetness="五分糖", toppings=None):
        if toppings is None:
            toppings = []

        # 基础热量
        total = self.drink.base_calories

        # 加糖度热量（简单的字典映射规则）
        sweet_rules = {"全糖": 100, "七分糖": 70, "五分糖": 50, "三分糖": 30, "无糖": 0}
        total += sweet_rules.get(sweetness, 50)

        # 加小料热量
        topping_rules = {"珍珠": 66, "椰果": 30, "奶盖": 80}
        for t in toppings:
            total += topping_rules.get(t, 0)

        return total


# 3. 文件读取（和之前一样）
def load_drinks(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"找不到文件：{filepath}")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 【关键变化】：把读出来的字典，转换成 Drink 对象！
            return [Drink(**item) for item in data]
    except json.JSONDecodeError:
        print("错误：JSON文件格式不正确！")
        return []


# 4. 测试运行
if __name__ == "__main__":
    filepath = "data/drinks.json"

    try:
        drinks_list = load_drinks(filepath)

        # 取出第一杯饮品（波霸奶茶）
        first_drink = drinks_list[0]

        # 把它交给计算器
        estimator = CalorieEstimator(first_drink)

        # 计算：三分糖 + 珍珠
        total_kcal = estimator.calculate(sweetness="三分糖", toppings=["珍珠"])

        print(f"饮品对象：{first_drink}")
        print(f"基础热量：{first_drink.base_calories} 大卡")
        print(f"选了【三分糖 + 珍珠】后，估算总热量：{total_kcal} 大卡")

    except FileNotFoundError as e:
        print(e)