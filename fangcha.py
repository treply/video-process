import statistics

# 定义5个数字
numbers = [0.35, 0.57, 0.48, 0.30, 0.59, 0.31]

# 计算平均值
mean = sum(numbers) / len(numbers)

# 计算每个数字与平均值的差的平方，并求和
sum_of_squares = sum((x - mean) ** 2 for x in numbers)

# 计算方差
variance = sum_of_squares / len(numbers)

print("方差是:", variance)
