import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置支持中文的字体，例如SimHei（黑体）
zh_font = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')

# 数据
data1 = [0.39, 0.64, 0.90, 1.28, 0.92, 0.89,1.16, 1.20, 0.79, 0.97, 0.74]
data2 = [0.18, 0.32, 0.41, 0.50, 0.40, 0.35, 0.57, 0.48, 0.30, 0.59, 0.31]
x_labels = range(1, 12)  # x轴标签从1到10

# 创建折线图，并设置图形大小
plt.figure(figsize=(11, 6))  # 调整图形大小，x轴长度为10，y轴长度为6
plt.plot(x_labels, data1, marker='o', markersize=5, label='UV', color='r')  # 调整markersize参数
plt.plot(x_labels, data2, marker='o', markersize=5, label='PV',color='pink')  # 调整markersize参数

# 设置x轴刻度和标签
plt.xticks(x_labels, [])  # 传递空列表以去掉x轴上的数字
plt.tick_params(axis='x', which='both', bottom=False, top=False)  # 去掉x轴的刻度线

# 设置y轴范围
plt.ylim(0, 1.3)  # y轴从0到0.013

# 添加标题和标签，并设置字体
plt.title('吸引度', fontproperties=zh_font, fontsize=16, fontweight='bold', y=1.05)  # 加大加粗标题并调高位置


# 添加水平虚线
plt.plot([1, 5], [0.83, 0.83], color='r', linestyle='--')  # 0.002的虚线在x轴的1-6
plt.plot([6, 11], [0.96, 0.96], color='r', linestyle='--')  # 0.0067的虚线在x轴的6-12



# 添加水平虚线
plt.plot([1, 5], [0.36, 0.36], color='pink', linestyle='--')  # 0.002的虚线在x轴的1-6
plt.plot([6, 11], [0.43, 0.43], color='pink', linestyle='--')  # 0.0067的虚线在x轴的6-12




# 在每个数据点上显示乘以100后的数值
for i, (x, y) in enumerate(zip(x_labels, data1)):
    if i == 3:  # 第4个数据点向下偏移
        y_offset = -0.08
    else:
        y_offset = 0.02  # 其他数据点向上偏移
    plt.text(x, y + y_offset, f'{y:.2f}', ha='center', va='bottom', fontsize=10)


for i, (x, y) in enumerate(zip(x_labels, data2)):
    y_offset = 0.02  # 数据点向上偏移
    plt.text(x, y + y_offset, f'{y:.2f}', ha='center', va='bottom', fontsize=10)

# 添加图例
plt.legend()

# 保存为PDF
plt.savefig('吸引度.png')

# 显示图形
plt.show()