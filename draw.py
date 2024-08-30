import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置支持中文的字体，例如SimHei（黑体）
zh_font = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')

# 数据
data = [0.0024, 0.0022, 0.0021, 0.0013, 0.0019, 0.0032, 0.0051, 0.0094, 0.0053, 0.0074, 0.0098]
x_labels = range(1, 12)  # x轴标签从1到10

# 创建折线图，并设置图形大小
plt.figure(figsize=(11, 6))  # 调整图形大小，x轴长度为10，y轴长度为6
plt.plot(x_labels, data, marker='o', markersize=5, color='#6495ED')  # 调整markersize参数

# 设置x轴刻度和标签
plt.xticks(x_labels, [])  # 传递空列表以去掉x轴上的数字
plt.tick_params(axis='x', which='both', bottom=False, top=False)  # 去掉x轴的刻度线

# 设置y轴范围
plt.ylim(0, 0.01)  # y轴从0到0.012，即0%到1.2%

# 添加标题和标签，并设置字体
plt.title('转化率', fontproperties=zh_font, fontsize=16, fontweight='bold', y=1.05)  # 加大加粗标题并调高位置

# 在纵轴的所有数字上加上百分号
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:.2%}".format(x)))

# 添加水平虚线
plt.plot([1, 5], [0.002, 0.002], color='#6495ED', linestyle='--')  # 0.002的虚线在x轴的1-6
plt.plot([6, 11], [0.0067, 0.0067], color='#6495ED', linestyle='--')  # 0.0067的虚线在x轴的6-12


# 在每个数据点上显示乘以100后的数值
for i, (x, y) in enumerate(zip(x_labels, data)):
    if i < len(data) - 1:
        y_offset = 0.0002  # 前10个数字向上偏移
    else:
        y_offset = -0.0006  # 最后一个数字向下偏移
    plt.text(x, y + y_offset, f'{y*100:.2f}%', ha='center', va='bottom', fontsize=10)

# 保存为PDF
plt.savefig('转化率.png')

# 显示图形
plt.show()